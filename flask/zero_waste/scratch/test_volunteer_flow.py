import urllib.request
import urllib.parse
import http.cookiejar
import re

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
        # 1. Get available deliveries
        with opener.open(f"{BASE_URL}/volunteer/dashboard") as response:
            html = response.read().decode('utf-8')
            # Look for task acceptance link
            match = re.search(r'/volunteer/accept/(\d+)', html)
            if match:
                task_id = match.group(1)
                print(f"  Found available task: {task_id}")
                
                # 2. Accept Task
                with opener.open(f"{BASE_URL}/volunteer/accept/{task_id}", b"") as accept_resp:
                    print(f"  [OK] Task {task_id} accepted.")
                
                # 3. Pick Up Food
                # Need to find the delivery ID. It's usually the same or I can find it in the dashboard.
                with opener.open(f"{BASE_URL}/volunteer/dashboard") as response:
                    html = response.read().decode('utf-8')
                    # Look for pickup link: /volunteer/pickup/<delivery_id>
                    pickup_match = re.search(r'/volunteer/pickup/(\d+)', html)
                    if pickup_match:
                        delivery_id = pickup_match.group(1)
                        print(f"  Found delivery ID: {delivery_id}. Picking up...")
                        with opener.open(f"{BASE_URL}/volunteer/pickup/{delivery_id}", b"") as pickup_resp:
                            print("  [OK] Food picked up.")
                            
                        # 4. Complete Delivery with OTP
                        # We need the OTP. I'll get it from the database via a sub-script or I can find it in NGO dashboard.
                        # For testing, I'll use a python one-liner to get the OTP for this delivery.
                        import subprocess
                        otp_cmd = f"python -c \"from app import create_app; from models.delivery import Delivery; app=create_app(); [print(d.otp) for d in app.app_context().push() or Delivery.query.filter_by(id={delivery_id}).all()]\""
                        otp = subprocess.check_output(otp_cmd, shell=True).decode('utf-8').strip()
                        print(f"  Retrieved OTP from DB: {otp}")
                        
                        # Post the OTP to complete delivery
                        complete_data = urllib.parse.urlencode({'otp': otp}).encode('utf-8')
                        with opener.open(f"{BASE_URL}/volunteer/complete/{delivery_id}", complete_data) as complete_resp:
                            if complete_resp.status == 200:
                                print("  [OK] Delivery COMPLETED with OTP!")
                                return True
                    else:
                        print("  [FAIL] Could not find pickup link in dashboard.")
            else:
                print("  [FAIL] No available tasks found for volunteer.")
    else:
        print("  [FAIL] Volunteer login failed.")
    return False

if __name__ == "__main__":
    test_full_delivery_flow()
