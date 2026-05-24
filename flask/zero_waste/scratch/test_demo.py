import urllib.request
import urllib.parse
import http.cookiejar
import re
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

def test_demo_sequence():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    
    # 1. DONOR LISTS FOOD
    print("Step 1: Donor listing food...")
    if login(opener, 'donor@test.com', 'password123'):
        expiry = (datetime.now() + timedelta(hours=4)).strftime('%Y-%m-%dT%H:%M')
        prepared = (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M')
        
        post_data = urllib.parse.urlencode({
            'title': 'Demo Feast',
            'food_type': 'Veg',
            'quantity': '20 packs',
            'temp_category': 'Hot',
            'prepared_at': prepared,
            'expiry_time': expiry,
            'liability_accepted': 'on'
        }).encode('utf-8')
        
        with opener.open(f"{BASE_URL}/donor/list-food", post_data) as response:
            if response.status == 200:
                print("  [OK] Food listed successfully.")
            else:
                print(f"  [FAIL] Failed to list food. Status: {response.status}")
    else:
        print("  [FAIL] Donor login failed.")
        return

    # 2. NGO CLAIMS FOOD
    print("\nStep 2: NGO claiming food...")
    cj.clear()
    if login(opener, 'ngo@test.com', 'password123'):
        # First, find the listing ID in the dashboard
        with opener.open(f"{BASE_URL}/ngo/dashboard") as response:
            html = response.read().decode('utf-8')
            match = re.search(r'/ngo/claim/(\d+)', html)
            if match:
                listing_id = match.group(1)
                print(f"  Found available listing ID: {listing_id}")
                
                # Claim it
                with opener.open(f"{BASE_URL}/ngo/claim/{listing_id}", b"") as claim_resp:
                    if claim_resp.status == 200:
                        print("  [OK] Food claimed successfully.")
                    else:
                        print(f"  [FAIL] Claim failed. Status: {claim_resp.status}")
            else:
                print("  [FAIL] No available food found to claim.")
    else:
        print("  [FAIL] NGO login failed.")

if __name__ == "__main__":
    test_demo_sequence()
