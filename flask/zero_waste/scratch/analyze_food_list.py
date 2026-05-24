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

print("Analyzing Available Food Section...")
try:
    with opener.open(LOGIN_URL, login_data) as response:
        html = response.read().decode('utf-8')
        
    start_idx = html.find('Available Food Near You')
    if start_idx != -1:
        print("Found 'Available Food Near You' section.")
        section_html = html[start_idx:start_idx+2000]
        
        # Look for the card content
        card_match = re.search(r'<h4.*?>(.*?)</h4>', section_html)
        if card_match:
            print(f"Food Title found: '{card_match.group(1).strip()}'")
            
            # Look for donor info
            donor_match = re.search(r'<i class="fa-solid fa-building".*?</i>\s*(.*?)\s*•', section_html, re.DOTALL)
            if donor_match:
                print(f"Donor Name found: '{donor_match.group(1).strip()}'")
            else:
                print("Donor Name NOT found in this section.")
                # Show the block
                building_idx = section_html.find('fa-building')
                if building_idx != -1:
                    print("Snippet around fa-building:")
                    print(section_html[building_idx-50:building_idx+150])
        else:
            print("No food titles found in available food section.")
    else:
        print("'Available Food Near You' section not found.")

except Exception as e:
    print(f"ERROR: {e}")
