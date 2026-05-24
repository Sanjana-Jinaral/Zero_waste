import urllib.request
import urllib.parse
import http.cookiejar

BASE_URL = 'http://127.0.0.1:5000'
LOGIN_URL = f'{BASE_URL}/auth/login'
DASHBOARD_URL = f'{BASE_URL}/ngo/dashboard'

# Set up cookie handler
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Login
login_data = urllib.parse.urlencode({
    'email': 'ngo@test.com',
    'password': 'password123'
}).encode('utf-8')

print(f"Attempting login as ngo@test.com...")
try:
    with opener.open(LOGIN_URL, login_data) as response:
        final_url = response.geturl()
        html = response.read().decode('utf-8')
        
    if response.status == 200 and '/ngo/dashboard' in final_url:
        print("SUCCESS: Logged in and redirected to NGO dashboard.")
        
        if 'NGO Dashboard' in html:
            print("SUCCESS: Found 'NGO Dashboard' heading.")
        else:
            print("FAILURE: 'NGO Dashboard' heading not found.")
            
        if 'id="map"' in html:
            print("SUCCESS: Found map container.")
        else:
            print("FAILURE: Map container not found.")
            
        if 'Available Food Near You' in html:
            print("SUCCESS: Found 'Available Food Near You' section.")
        else:
            print("FAILURE: 'Available Food Near You' section not found.")
    else:
        print(f"FAILURE: Login failed. Status: {response.status}, URL: {final_url}")
except Exception as e:
    print(f"ERROR: {e}")
