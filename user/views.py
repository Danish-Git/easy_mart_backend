from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from core.models.user import update_user, get_user_by_phone
from core.utils import validate_jwt_token  

@method_decorator(csrf_exempt, name='dispatch')
class UpdateProfileView(View):
    def post(self, request):
        # Get the JWT token from the Authorization header
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({"error": "Token is required"}, status=400)

        # Extract token (assuming it's "Bearer <token>")
        token = token.split(' ')[1]
        user_data = validate_jwt_token(token)  # Use the validate_jwt_token function

        if not user_data:
            return JsonResponse({"error": "Invalid or expired token"}, status=401)

        # User object fetched from the validate_jwt_token function
        phone = user_data.phone
        user = get_user_by_phone(phone)

        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        # Get data from the request body
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        profile_photo = request.POST.get('profile_photo')
        profile_photo_url = request.POST.get('profile_photo_url')
        primary_address = request.POST.get('primary_address')

        if not first_name:  # First name is required
            return JsonResponse({"error": "First name is required"}, status=400)

                # Use existing values if any fields are missing
        updated_data = {
            'first_name': first_name if first_name else user.first_name,
            'last_name': last_name if last_name else user.last_name,
            'profile_photo': profile_photo if profile_photo else user.profile_photo,
            'profile_photo_url': profile_photo_url if profile_photo_url else user.profile_photo_url,
            'primary_address': primary_address if primary_address else user.primary_address
        }

        # Filter out empty values
        updated_data = {key: value for key, value in updated_data.items() if value}
        
        # Use the update_user function to update the profile with the prepared data
        updated_user = update_user(
            phone = phone, 
            otp = user.otp, 
            first_name = updated_data['first_name'],
            last_name = updated_data['last_name'],
            primary_address = updated_data['primary_address'],
            profile_photo = updated_data['profile_photo'],
            profile_photo_url = updated_data['profile_photo_url'],
            is_verified = user.is_verified
        )


        if updated_user:
            # Manually update the fields in the user object
            for field, value in updated_data.items():
                setattr(updated_user, field, value)

            return JsonResponse({"message": "Profile updated successfully"}, status=200)

        return JsonResponse({"error": "Failed to update profile"}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class GetUserDetailsView(View):
    def get(self, request):
        # Get the JWT token from the Authorization header
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({"error": "Token is required"}, status=400)

        # Extract token (assuming it's "Bearer <token>")
        token = token.split(' ')[1]
        user_data = validate_jwt_token(token)  # Validate JWT token

        if not user_data:
            return JsonResponse({"error": "Invalid or expired token"}, status=401)

        # Get user by phone
        phone = user_data.phone
        user = get_user_by_phone(phone)

        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        # Prepare user details response
        user_details = {
            "phone": user.phone,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile_photo": {
                "id": str(user.profile_photo.id),
                "category": user.profile_photo.category,
                "url": user.profile_photo.image_url
            } if user.profile_photo else None,
            "profile_photo_url": user.profile_photo_url if user.profile_photo_url else None,
            "primary_address": {
                "id": str(user.primary_address.id),
                "address_line1": user.primary_address.address_line1,
                "address_line2": user.primary_address.address_line2,
                "city": user.primary_address.city,
                "state": user.primary_address.state,
                "postal_code": user.primary_address.postal_code
            } if user.primary_address else None,
            "is_verified": user.is_verified,
            "created_at": user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": user.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        return JsonResponse({"message": "User details retrieved successfully", "data": user_details}, status=200)
