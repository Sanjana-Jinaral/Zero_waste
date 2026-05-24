import urllib.request
import urllib.parse
import http.cookiejar
import re
import subprocess

BASE_URL = 'http://127.0.0.1:5000'

def login(opener, email, password):
    login_data = urllib.parse.urlencode({'email': email, 'password': password}).encode('utf-8')
    try:
        with opener.open(f"{BASE_URL}/auth/login", login_data) as response:
            if response.status == 200 and 'login' not in response.geturl().lower():
                return True
    except Exception as e:
        return False

def test_full_delivery_flow():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    
    print("Step 1: Volunteer finding and accepting a task...")
    if login(opener, 'volunteer@test.com', 'password123'):
        # 1. Get available tasks
        with opener.open(f"{BASE_URL}/volunteer/dashboard") as response:
            html = response.read().decode('utf-8')
            # The accept link is usually in a form or link. Let's look for /volunteer/accept/(\d+)
            match = re.search(r'/volunteer/accept/(\d+)', html)
            if match:
                claim_id = match.group(1)
                print(f"  Found available task for Claim ID: {claim_id}")
                
                # Accept Task (POST)
                with opener.open(f"{BASE_URL}/volunteer/accept/{claim_id}", b"") as accept_resp:
                    print(f"  [OK] Task for Claim {claim_id} accepted.")
            else:
                print("  [INFO] No new tasks found. Checking for existing active tasks...")

        # 2. Pick Up Food
        with opener.open(f"{BASE_URL}/volunteer/dashboard") as response:
            html = response.read().decode('utf-8')
            # Look for pickup form action: /volunteer/pickup/(\d+)
            pickup_match = re.search(r'/volunteer/pickup/(\d+)', html)
            if pickup_match:
                delivery_id = pickup_match.group(1)
                print(f"  Found delivery ID: {delivery_id}. Picking up...")
                # POST to pickup
                with opener.open(f"{BASE_URL}/volunteer/pickup/{delivery_id}", b"") as pickup_resp:
                    print("  [OK] Food picked up.")
            else:
                print("  [INFO] No 'Assigned' tasks found. Checking if already 'Picked Up'...")

        # 3. Complete Delivery with OTP
        with opener.open(f"{BASE_URL}/volunteer/dashboard") as response:
            html = response.read().decode('utf-8')
            # Look for complete form action: /volunteer/complete/(\d+)
            complete_match = re.search(r'/volunteer/complete/(\d+)', html)
            if complete_match:
                delivery_id = complete_match.group(1)
                print(f"  Found delivery ID {delivery_id} ready for completion.")
                
                # Get OTP from DB
                otp_cmd = f"python -c \"from app import create_app; from models.delivery import Delivery; app=create_app(); [print(d.otp) for d in app.app_context().push() or Delivery.query.filter_by(id={delivery_id}).all()]\""
                otp = subprocess.check_output(otp_cmd, shell=True).decode('utf-8').strip()
                print(f"  Retrieved OTP from DB: {otp}")
                
                # Post the OTP
                complete_data = urllib.parse.urlencode({'otp': otp}).encode('utf-8')
                with opener.open(f"{BASE_URL}/volunteer/complete/{delivery_id}", complete_data) as complete_resp:
                    if complete_resp.status == 200:
                        print("  [OK] Delivery COMPLETED with OTP verification!")
                        return True
            else:
                print("  [FAIL] No tasks in 'Picked Up' status found.")
    else:
        print("  [FAIL] Volunteer login failed.")
    return False

if __name__ == "__main__":
    test_full_delivery_flow()
