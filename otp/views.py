import random
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core.db_operations.user import save_user, get_user_by_phone, phone_exists, update_user
from core.utils import send_otp_via_fazpass
from core.utils import verify_otp_via_fazpass
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

        # Send OTP via Fazpass
        fazpass_response = send_otp_via_fazpass(phone_number)
        if not fazpass_response.get("status"):
            return JsonResponse({"error": "Failed to send OTP via Fazpass"}, status=500)

        # Extract OTP from response (if needed for development purposes)
        otp = fazpass_response.get("data", {}).get("id")

        # Save OTP and phone number in the database
        save_user(phone_number, otp)

        return JsonResponse({
            "message": "OTP sent successfully",
            "data": {
                "id": fazpass_response.get("data", {}).get("id"),
                "otp_length": fazpass_response.get("data", {}).get("otp_length"),
                "channel": fazpass_response.get("data", {}).get("channel"),
                "provider": fazpass_response.get("data", {}).get("provider"),
                "purpose": fazpass_response.get("data", {}).get("purpose")
            }
        })
    
    
@method_decorator(csrf_exempt, name='dispatch')
class VerifyOtpView(View):
    def post(self, request):
        phone_no = request.POST.get('phone_no')
        otp_id = request.POST.get('otp_id')
        otp = request.POST.get('otp')

        if not otp_id or not otp:
            return JsonResponse({"error": "Phone number and OTP are required"}, status=400)

        user = get_user_by_phone(phone_no, otp_id)

        # Verify OTP via Fazpass
        fazpass_response = verify_otp_via_fazpass(otp_id, otp)

        if not fazpass_response.get("status"):
            return JsonResponse({"error": "Failed to verify OTP via Fazpass"}, status=500)

        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        if user.otp == otp:
            # Update the user to mark OTP as verified
            update_user(phone_number, otp, is_verified=True)
            return JsonResponse({"message": "OTP verified successfully"})
        else:
            return JsonResponse({"error": "Invalid OTP"}, status=400)
