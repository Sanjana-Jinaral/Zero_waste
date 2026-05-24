import urllib.request
import urllib.parse
import http.cookiejar
import re

BASE_URL = 'http://127.0.0.1:5000'
LOGIN_URL = f'{BASE_URL}/auth/login'

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

login_data = urllib.parse.urlencode({
    'email': 'ngo@test.com',
    'password': 'password123'
}).encode('utf-8')

print("Debugging NGO Dashboard...")
try:
    with opener.open(LOGIN_URL, login_data) as response:
        html = response.read().decode('utf-8')
        
    # Find the donor name using regex
    match = re.search(r'<i class="fa-solid fa-building".*?</i>\s*(.*?)\s*•', html, re.DOTALL)
    if match:
        print(f"Found Donor Name in HTML: '{match.group(1).strip()}'")
    else:
        print("Could not find Donor Name pattern in HTML.")
        # Print a larger chunk around where it should be
        idx = html.find('MG Road, Bangalore')
        if idx != -1:
            print("Snippet around Address:")
            print(html[idx-200:idx+200])

except Exception as e:
    print(f"ERROR: {e}")
