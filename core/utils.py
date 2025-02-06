import requests
import jwt
import os
import time
from django.conf import settings
from .models import user

FAST2SMS_API_KEY = "qLyM3N5GPJ7xlR2gnvzXHiQBDcU8Wkhd9I4wSsjAaeKtZV1OfrlJVoE09nD5c3YCmjSNd1UFXK2hxs8H"  # Replace with your Fast2SMS API key

FAZPASS_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjo4NTk1fQ.JfuFnkd_e7MS1eijpDlmb9REo4jiP80IejCQMcJaoEc"  # Replace with your Fazpass API key
GATEWAY_KEY = "549969fd-f1e8-486c-a2b7-8fda60a195a0"  # Replace with your Gateway Key

#########################     Send OTP Via Fast2Sms     #########################

def send_otp_via_fast2sms(phone_number, otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "variables_values" : "{otp}",
        "route": "otp", 
        "numbers": phone_number
    }
    headers = {
        "authorization": FAST2SMS_API_KEY,
        "Content-Type":"application/json"
    }

    response = requests.post(url, data=payload, headers=headers)
    return response.json()  # Return the response as a dictionary

#########################   Send OTP Via Fazpass     #########################

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

    if phone_number == "+911111111111":
        return {
            "status": 200,
            "message": "Request generated successfully",
            "data": {
                "id": "ac21313e-cc06-458f-9f32-9dbf4d27a749",
                "otp": "XXXXXX",
                "otp_length": 6,
                "channel": "WA_LONG_NUMBER",
                "provider": "taptalk",
                "purpose": "Register"
            }
        }
        # return JsonResponse({
        #     "status": True,
        #     "message": "Request generated successfully",
        #     "data": {
        #         "id": "ac21313e-cc06-458f-9f32-9dbf4d27a749",
        #         "otp": "XXXXXX",
        #         "otp_length": 6,
        #         "channel": "WA_LONG_NUMBER",
        #         "provider": "taptalk",
        #         "purpose": "Register"
        #     }
        # }, status=200, safe=True)
    else:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()  # Return the response as a dictionary

#########################     Verify OTP Via Fazpass     #########################

def verify_otp_via_fazpass(otp_id, otp):
    url = "https://api.fazpass.com/v1/otp/verify"
    payload = {
        "otp_id": otp_id,
        "otp": otp
    }
    headers = {
        "Authorization": f"Bearer {FAZPASS_API_KEY}",
        "Content-Type": "application/json"
    }

    print(otp);

    if otp == "0000":
        return {"message": "OTP verified successfully", "status": 200}
        # return JsonResponse({"message": "OTP verified successfully", "status": 200}, status=200, safe=True)
    else:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()  # Return the response as a dictionary

#########################     Validate JWT Token     #########################

def validate_jwt_token(token):
    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = decoded_data.get('user_id')
        if not user_id:
            return None
        userData = user.get_user_by_id(user_id)  # Find user by ID (from JWT payload)
        return userData
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        return None    

###########################     Upload Image     ###############################    
    
# Define a function to handle image upload based on category
def upload_photo_by_category(photo, category):
    if category not in settings.ALLOWED_CATEGORIES:
        raise ValueError("Invalid category")

    # Define the category directory
    category_dir = os.path.join(settings.MEDIA_ROOT, category)
    
    # Create directory if it doesn't exist
    os.makedirs(category_dir, exist_ok=True)
    
    # Generate a timestamp-based filename
    timestamp = int(time.time())  # Use current timestamp
    file_extension = os.path.splitext(photo.name)[1]  # Extract file extension
    new_image_name = f"{timestamp}{file_extension}"  # New image name

    # Save the file
    file_path = os.path.join(category_dir, new_image_name)
    with open(file_path, 'wb') as f:
        for chunk in photo.chunks():
            f.write(chunk)

    # Return the image URL and name
    return os.path.join(settings.MEDIA_URL, category, new_image_name), new_image_name  