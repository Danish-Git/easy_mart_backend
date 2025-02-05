import requests

FAST2SMS_API_KEY = "qLyM3N5GPJ7xlR2gnvzXHiQBDcU8Wkhd9I4wSsjAaeKtZV1OfrlJVoE09nD5c3YCmjSNd1UFXK2hxs8H"  # Replace with your Fast2SMS API key

def send_otp_via_fast2sms(phone_number, otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "sender_id": "FSTSMS", 
        "message": f"Your OTP is {otp}",
        "language": "english",
        "route": "p", 
        "numbers": phone_number
    }
    headers = {
        "authorization": FAST2SMS_API_KEY
    }

    response = requests.post(url, data=payload, headers=headers)
    return response.json()  # Return the response as a dictionary
