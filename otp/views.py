# from django.http import JsonResponse
# from django.views import View
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt

# @method_decorator(csrf_exempt, name='dispatch')
# class SendOtpView(View):
#     def get(self, request):
#         return JsonResponse({"message": "Hello World from GET"})

#     def post(self, request):
#         return JsonResponse({"message": "Hello World from POST"})


import random
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core.db_operations.user import save_user, get_user_by_phone, phone_exists, update_user
from core.utils import send_otp_via_fast2sms
from datetime import datetime

@method_decorator(csrf_exempt, name='dispatch')
class SendOtpView(View):
    def post(self, request):
        # Get phone number from the request body
        phone_number = request.POST.get('phone_number')

        if not phone_number:
            return JsonResponse({"error": "Phone number is required"}, status=400)

        # Check if phone number already exists
        if phone_exists(phone_number):
            return JsonResponse({"error": "Phone number already exists"}, status=400)

        # Generate a random OTP
        otp = str(random.randint(100000, 999999))

        # Send OTP via Fast2SMS
        fast2sms_response = send_otp_via_fast2sms(phone_number, otp)
        if fast2sms_response.get("message") != "success":
            return JsonResponse({"error": "Failed to send OTP via Fast2SMS"}, status=500)

        # Save OTP and phone number in the database
        save_user(phone_number, otp)

        return JsonResponse({"message": "OTP sent successfully"})

class VerifyOtpView(View):
    def post(self, request):
        phone_number = request.POST.get('phone_number')
        otp = request.POST.get('otp')

        if not phone_number or not otp:
            return JsonResponse({"error": "Phone number and OTP are required"}, status=400)

        user = get_user_by_phone(phone_number)
        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        if user.otp == otp:
            # Update the user to mark OTP as verified
            update_user(phone_number, otp, is_verified=True)
            return JsonResponse({"message": "OTP verified successfully"})
        else:
            return JsonResponse({"error": "Invalid OTP"}, status=400)
