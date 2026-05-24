import urllib.request
import urllib.parse
import http.cookiejar
import re
import subprocess

BASE_URL = 'http://127.0.0.1:5000'

def get_opener():
    cj = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def login(opener, email, password):
    login_data = urllib.parse.urlencode({'email': email, 'password': password}).encode('utf-8')
    opener.open(f"{BASE_URL}/auth/login", login_data)

def run_full_cycle():
    # 1. NGO CLAIMS
    print("NGO claiming food...")
    ngo_opener = get_opener()
    login(ngo_opener, 'ngo@test.com', 'password123')
    with ngo_opener.open(f"{BASE_URL}/ngo/dashboard") as resp:
        html = resp.read().decode('utf-8')
        match = re.search(r'/ngo/claim/(\d+)', html)
        if not match:
            print("No food available to claim!")
            return
        listing_id = match.group(1)
    ngo_opener.open(f"{BASE_URL}/ngo/claim/{listing_id}", b"")
    print(f"Claimed Listing {listing_id}")

    # 2. VOLUNTEER ACCEPTS
    print("Volunteer accepting task...")
    vol_opener = get_opener()
    login(vol_opener, 'volunteer@test.com', 'password123')
    with vol_opener.open(f"{BASE_URL}/volunteer/dashboard") as resp:
        html = resp.read().decode('utf-8')
        match = re.search(r'/volunteer/accept/(\d+)', html)
        if not match:
            print("No task available to accept!")
            return
        claim_id = match.group(1)
    vol_opener.open(f"{BASE_URL}/volunteer/accept/{claim_id}", b"")
    
    # 3. GET DELIVERY ID
    with vol_opener.open(f"{BASE_URL}/volunteer/dashboard") as resp:
        html = resp.read().decode('utf-8')
        match = re.search(r'/volunteer/confirm-pickup/(\d+)', html)
        if not match:
            print("No delivery found to pickup!")
            return
        delivery_id = match.group(1)
    
    # 4. PICKUP
    print(f"Picking up Delivery {delivery_id}...")
    vol_opener.open(f"{BASE_URL}/volunteer/confirm-pickup/{delivery_id}", b"")
    
    # 5. GET OTP
    otp_cmd = f"python -c \"from app import create_app; from models.delivery import Delivery; app=create_app(); [print(d.otp) for d in app.app_context().push() or Delivery.query.filter_by(id={delivery_id}).all()]\""
    otp = subprocess.check_output(otp_cmd, shell=True).decode('utf-8').strip()
    print(f"OTP is {otp}")
    
    # 6. COMPLETE
    print("Completing delivery...")
    complete_data = urllib.parse.urlencode({'otp': otp}).encode('utf-8')
    response = vol_opener.open(f"{BASE_URL}/volunteer/complete/{delivery_id}", complete_data)
    if response.status == 200:
        print("SUCCESS: Full cycle completed!")

if __name__ == "__main__":
    run_full_cycle()
