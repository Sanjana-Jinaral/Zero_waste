import urllib.request
import urllib.parse
import http.cookiejar
import re
from datetime import datetime, timedelta
import time

BASE_URL = 'http://127.0.0.1:5000'

def login(opener, email, password):
    login_data = urllib.parse.urlencode({'email': email, 'password': password}).encode('utf-8')
    try:
        with opener.open(f"{BASE_URL}/auth/login", login_data) as response:
            if response.status == 200 and 'login' not in response.geturl().lower():
                return True
    except Exception as e:
        return False

def run_once(iteration):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    
    print(f"\n--- TEST ITERATION {iteration}/6 ---")
    
    # 1. DONOR LISTS FOOD
    if login(opener, 'donor@test.com', 'password123'):
        expiry = (datetime.now() + timedelta(hours=4)).strftime('%Y-%m-%dT%H:%M')
        post_data = urllib.parse.urlencode({
            'title': f'Stress Test Food {iteration}',
            'food_type': 'Veg',
            'quantity': f'{iteration} kg',
            'expiry_time': expiry,
            'liability_accepted': 'on'
        }).encode('utf-8')
        
        with opener.open(f"{BASE_URL}/donor/list-food", post_data) as response:
            if response.status == 200:
                print(f"  [OK] Iteration {iteration}: Food listed.")
            else:
                print(f"  [FAIL] Iteration {iteration}: Listing failed.")
                return False
    else:
        print(f"  [FAIL] Iteration {iteration}: Donor login failed.")
        return False

    # 2. NGO CLAIMS FOOD
    cj.clear()
    if login(opener, 'ngo@test.com', 'password123'):
        with opener.open(f"{BASE_URL}/ngo/dashboard") as response:
            html = response.read().decode('utf-8')
            match = re.search(r'/ngo/claim/(\d+)', html)
            if match:
                listing_id = match.group(1)
                with opener.open(f"{BASE_URL}/ngo/claim/{listing_id}", b"") as claim_resp:
                    if claim_resp.status == 200:
                        print(f"  [OK] Iteration {iteration}: Food claimed (ID: {listing_id}).")
                        return True
                    else:
                        print(f"  [FAIL] Iteration {iteration}: Claim failed.")
            else:
                print(f"  [FAIL] Iteration {iteration}: No available food found.")
    else:
        print(f"  [FAIL] Iteration {iteration}: NGO login failed.")
    return False

if __name__ == "__main__":
    success_count = 0
    for i in range(1, 7):
        if run_once(i):
            success_count += 1
        time.sleep(1) # Small delay between tests
    
    print(f"\nSTRESS TEST COMPLETE: {success_count}/6 Successes.")
