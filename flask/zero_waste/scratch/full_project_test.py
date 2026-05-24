import urllib.request
import urllib.parse
import http.cookiejar
import re
import json
import subprocess
from datetime import datetime, timedelta

BASE_URL = 'http://127.0.0.1:5000'

def login(opener, email, password):
    login_data = urllib.parse.urlencode({'email': email, 'password': password}).encode('utf-8')
    try:
        with opener.open(f"{BASE_URL}/auth/login", login_data) as response:
            if response.status == 200 and 'login' not in response.geturl().lower():
                return True
    except Exception as e:
        print(f"Login Error ({email}): {e}")
    return False

def test_full_cycle():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    
    print("--- STARTING FULL CYCLE TEST ---")
    
    # 1. DONOR LISTS FOOD
    print("\n[STEP 1] Donor listing food...")
    if login(opener, 'donor@test.com', 'password123'):
        expiry = (datetime.now() + timedelta(hours=4)).strftime('%Y-%m-%dT%H:%M')
        prepared = (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M')
        
        post_data = urllib.parse.urlencode({
            'title': 'Test Banquet',
            'food_type': 'Veg',
            'quantity': '15 kg',
            'temp_category': 'Cold',
            'prepared_at': prepared,
            'expiry_time': expiry,
            'liability_accepted': 'on'
        }).encode('utf-8')
        
        with opener.open(f"{BASE_URL}/donor/list-food", post_data) as response:
            if response.status == 200:
                print("  [SUCCESS] Food listed.")
            else:
                print(f"  [FAILED] Food listing. Status: {response.status}")
                return
    else:
        print("  [FAILED] Donor login.")
        return

    # 2. NGO CLAIMS FOOD
    print("\n[STEP 2] NGO claiming food...")
    cj.clear() # Clear donor cookies
    if login(opener, 'ngo@test.com', 'password123'):
        with opener.open(f"{BASE_URL}/ngo/dashboard") as response:
            html = response.read().decode('utf-8')
            match = re.search(r'/ngo/claim/(\d+)', html)
            if match:
                listing_id = match.group(1)
                print(f"  Found listing ID: {listing_id}. Claiming...")
                with opener.open(f"{BASE_URL}/ngo/claim/{listing_id}", b"") as claim_resp:
                    if claim_resp.status == 200:
                        print("  [SUCCESS] Food claimed.")
                    else:
                        print(f"  [FAILED] Claiming food. Status: {claim_resp.status}")
                        return
            else:
                print("  [FAILED] No listing found to claim.")
                return
    else:
        print("  [FAILED] NGO login.")
        return

    # 3. VOLUNTEER FLOW
    print("\n[STEP 3] Volunteer flow (Accept -> Pickup -> Deliver)...")
    cj.clear() # Clear NGO cookies
    if login(opener, 'volunteer@test.com', 'password123'):
        # 3a. Accept
        with opener.open(f"{BASE_URL}/volunteer/dashboard") as response:
            html = response.read().decode('utf-8')
            accept_match = re.search(r'/volunteer/accept/(\d+)', html)
            if accept_match:
                task_id = accept_match.group(1)
                print(f"  Accepting Task ID: {task_id}")
                opener.open(f"{BASE_URL}/volunteer/accept/{task_id}", b"")
                print("  [SUCCESS] Task accepted.")
            else:
                print("  [FAILED] No task found to accept.")
                return
        
        # 3b. Pickup
        with opener.open(f"{BASE_URL}/volunteer/dashboard") as response:
            html = response.read().decode('utf-8')
            # Look for pickup link: /volunteer/confirm-pickup/<delivery_id>
            pickup_match = re.search(r'/volunteer/confirm-pickup/(\d+)', html)
            if pickup_match:
                delivery_id = pickup_match.group(1)
                print(f"  Picking up Delivery ID: {delivery_id}")
                # It's a POST request
                opener.open(f"{BASE_URL}/volunteer/confirm-pickup/{delivery_id}", b"")
                print("  [SUCCESS] Food picked up.")
            else:
                print("  [FAILED] No pickup link found.")
                return

        # 3c. Deliver with OTP
        # Retrieve OTP from DB
        try:
            otp_cmd = f"python -c \"from app import create_app; from models.delivery import Delivery; app=create_app(); [print(d.otp) for d in app.app_context().push() or Delivery.query.filter_by(id={delivery_id}).all()]\""
            otp = subprocess.check_output(otp_cmd, shell=True).decode('utf-8').strip()
            print(f"  OTP retrieved from DB: {otp}")
            
            complete_data = urllib.parse.urlencode({'otp': otp}).encode('utf-8')
            with opener.open(f"{BASE_URL}/volunteer/complete/{delivery_id}", complete_data) as complete_resp:
                if complete_resp.status == 200:
                    print("  [SUCCESS] Delivery COMPLETED with OTP!")
                else:
                    print(f"  [FAILED] Completing delivery. Status: {complete_resp.status}")
        except Exception as e:
            print(f"  [FAILED] OTP retrieval or delivery completion: {e}")
    else:
        print("  [FAILED] Volunteer login.")
        return

    print("\n--- FULL CYCLE TEST COMPLETED SUCCESSFULLY ---")

if __name__ == "__main__":
    test_full_cycle()
