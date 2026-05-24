import urllib.request
import urllib.parse
import http.cookiejar
import subprocess

BASE_URL = 'http://127.0.0.1:5000'

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def login():
    login_data = urllib.parse.urlencode({'email': 'volunteer@test.com', 'password': 'password123'}).encode('utf-8')
    opener.open(f"{BASE_URL}/auth/login", login_data)

def finish_delivery(delivery_id):
    # 1. Pick Up
    print(f"Picking up delivery {delivery_id}...")
    opener.open(f"{BASE_URL}/volunteer/pickup/{delivery_id}", b"")
    
    # 2. Get OTP
    otp_cmd = f"python -c \"from app import create_app; from models.delivery import Delivery; app=create_app(); [print(d.otp) for d in app.app_context().push() or Delivery.query.filter_by(id={delivery_id}).all()]\""
    otp = subprocess.check_output(otp_cmd, shell=True).decode('utf-8').strip()
    print(f"OTP is {otp}")
    
    # 3. Complete
    print("Completing delivery...")
    complete_data = urllib.parse.urlencode({'otp': otp}).encode('utf-8')
    response = opener.open(f"{BASE_URL}/volunteer/complete/{delivery_id}", complete_data)
    if response.status == 200:
        print("SUCCESS: Delivery completed!")

if __name__ == "__main__":
    login()
    finish_delivery(1) # Finish the first one
