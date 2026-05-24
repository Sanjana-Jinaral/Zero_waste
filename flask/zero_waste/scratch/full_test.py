import urllib.request
import urllib.parse
import http.cookiejar
import re

BASE_URL = 'http://127.0.0.1:5000'

def test_page(opener, path, name):
    print(f"Testing {name} ({path})...")
    try:
        with opener.open(f"{BASE_URL}{path}") as response:
            if response.status == 200:
                print(f"  [OK] {name} loaded.")
                return response.read().decode('utf-8')
            else:
                print(f"  [FAIL] {name} returned status {response.status}")
    except Exception as e:
        print(f"  [ERROR] {name}: {e}")
    return None

def login(opener, email, password):
    login_data = urllib.parse.urlencode({'email': email, 'password': password}).encode('utf-8')
    try:
        with opener.open(f"{BASE_URL}/auth/login", login_data) as response:
            if response.status == 200 and 'login' not in response.geturl().lower():
                return True
    except Exception as e:
        print(f"Login Error ({email}): {e}")
    return False

def run_tests():
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    
    # 1. Landing Page
    test_page(opener, "/", "Landing Page")
    
    # 2. Donor Flow
    print("\n--- Testing Donor Flow ---")
    if login(opener, 'donor@test.com', 'password123'):
        print("  [OK] Donor Login.")
        html = test_page(opener, "/donor/dashboard", "Donor Dashboard")
        if html and 'My Food Listings' in html:
            print("  [OK] Donor Dashboard Content Verified.")
    else:
        print("  [FAIL] Donor Login.")
        
    # 3. NGO Flow
    print("\n--- Testing NGO Flow ---")
    cj.clear() # Clear cookies for new user
    if login(opener, 'ngo@test.com', 'password123'):
        print("  [OK] NGO Login.")
        html = test_page(opener, "/ngo/dashboard", "NGO Dashboard")
        if html and 'NGO Dashboard' in html:
            print("  [OK] NGO Dashboard Content Verified.")
    else:
        print("  [FAIL] NGO Login.")
        
    # 4. Volunteer Flow
    print("\n--- Testing Volunteer Flow ---")
    cj.clear()
    if login(opener, 'volunteer@test.com', 'password123'):
        print("  [OK] Volunteer Login.")
        html = test_page(opener, "/volunteer/dashboard", "Volunteer Dashboard")
        if html and 'Volunteer Dashboard' in html:
            print("  [OK] Volunteer Dashboard Content Verified.")
    else:
        print("  [FAIL] Volunteer Login.")

if __name__ == "__main__":
    run_tests()
