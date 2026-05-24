import urllib.request
import urllib.parse
import http.cookiejar

BASE_URL = 'http://127.0.0.1:5000'
LOGIN_URL = f'{BASE_URL}/auth/login'

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

login_data = urllib.parse.urlencode({
    'email': 'ngo@test.com',
    'password': 'password123'
}).encode('utf-8')

print("Testing NGO Dashboard...")
try:
    with opener.open(LOGIN_URL, login_data) as response:
        html = response.read().decode('utf-8')
        final_url = response.geturl()
        
    if response.status == 200 and '/ngo/dashboard' in final_url:
        print("✅ Login Successful.")
        
        checks = {
            'Dashboard Title': 'NGO Dashboard',
            'Map Container': 'id="map"',
            'Food List': 'Available Food Near You',
            'Donor Info': 'Empire Restaurant', # From seed data
            'Address Info': 'MG Road, Bangalore'  # From seed data
        }
        
        for name, snippet in checks.items():
            if snippet in html:
                print(f"✅ {name} found.")
            else:
                print(f"❌ {name} NOT found.")
                # Print a bit of context if it's a critical failure
                if name == 'Dashboard Title':
                    print(f"Content snippet: {html[:200]}")
    else:
        print(f"❌ Login failed or redirected incorrectly. Status: {response.status}, URL: {final_url}")

except Exception as e:
    print(f"💥 ERROR during test: {e}")
