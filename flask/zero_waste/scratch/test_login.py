import requests

BASE_URL = 'http://127.0.0.1:5000'
LOGIN_URL = f'{BASE_URL}/auth/login'
DASHBOARD_URL = f'{BASE_URL}/ngo/dashboard'

# Start a session
session = requests.Session()

# 1. Login
login_data = {
    'email': 'ngo@test.com',
    'password': 'password123'
}

print(f"Attempting login as {login_data['email']}...")
response = session.post(LOGIN_URL, data=login_data, allow_redirects=True)

if response.status_code == 200 and '/ngo/dashboard' in response.url:
    print("SUCCESS: Logged in and redirected to NGO dashboard.")
    
    # 2. Check content
    if 'NGO Dashboard' in response.text:
        print("SUCCESS: Found 'NGO Dashboard' heading.")
    else:
        print("FAILURE: 'NGO Dashboard' heading not found.")
        
    if 'id="map"' in response.text:
        print("SUCCESS: Found map container.")
    else:
        print("FAILURE: Map container not found.")
        
    if 'Available Food Near You' in response.text:
        print("SUCCESS: Found 'Available Food Near You' section.")
    else:
        print("FAILURE: 'Available Food Near You' section not found.")
else:
    print(f"FAILURE: Login failed. Status: {response.status_code}, URL: {response.url}")
    if response.status_code == 200:
        print("Maybe check if Flash messages say anything?")
        if 'Invalid email or password' in response.text:
            print("Message: Invalid email or password")
