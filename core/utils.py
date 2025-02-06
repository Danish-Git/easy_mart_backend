# import requests

# FAST2SMS_API_KEY = "qLyM3N5GPJ7xlR2gnvzXHiQBDcU8Wkhd9I4wSsjAaeKtZV1OfrlJVoE09nD5c3YCmjSNd1UFXK2hxs8H"  # Replace with your Fast2SMS API key

# def send_otp_via_fast2sms(phone_number, otp):
#     url = "https://www.fast2sms.com/dev/bulkV2"
#     payload = {
#         "variables_values" : "{otp}",
#         "route": "otp", 
#         "numbers": phone_number
#     }
#     headers = {
#         "authorization": FAST2SMS_API_KEY,
#         "Content-Type":"application/json"
#     }

#     response = requests.post(url, data=payload, headers=headers)
#     return response.json()  # Return the response as a dictionary


import requests
from django.http import JsonResponse

FAZPASS_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjo4NTk1fQ.JfuFnkd_e7MS1eijpDlmb9REo4jiP80IejCQMcJaoEc"  # Replace with your Fazpass API key
GATEWAY_KEY = "549969fd-f1e8-486c-a2b7-8fda60a195a0"  # Replace with your Gateway Key

def send_otp_via_fazpass(phone_number):
    url = "https://api.fazpass.com/v1/otp/request"
    payload = {
        "phone": phone_number,
        "gateway_key": GATEWAY_KEY,
        "params": [
            {
                "tag": "brand",
                "value": "Easy Mart"
            }
        ]
    }
    headers = {
        "Authorization": f"Bearer {FAZPASS_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()  # Return the response as a dictionary

# def verify_otp_via_fazpass(otp_id, otp):
#     url = "https://api.fazpass.com/v1/otp/verify"
#     payload = {
#         "otp_id": otp_id,
#         "otp": otp
#     }
#     headers = {
#         "Authorization": f"Bearer {FAZPASS_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     response = requests.post(url, json=payload, headers=headers)
#     return response.json()  # Return the response as a dictionary

def verify_otp_via_fazpass(otp_id, otp):
    # Mock response for testing
    if otp == "123456":  # Assume "123456" is the correct OTP for testing
        mock_response = {
            "status": True,
            "message": "OTP verified successfully",
            "data": {
                "otp_id": otp_id,
                "phone_no": "+1234567890"  # Mock phone number
            }
        }
    else:
        mock_response = {
            "status": False,
            "message": "Invalid OTP"
        }

    # Simulate an HTTP response object
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        @property
        def content(self):
            return json.dumps(self.json_data).encode('utf-8')

    return MockResponse(mock_response, 200 if mock_response["status"] else 400)