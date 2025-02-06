# views.py
from django.http import JsonResponse
from django.views import View
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
        profile_photo_id = request.POST.get('profile_photo_id')
        profile_photo_url = request.POST.get('profile_photo_url')
        primary_address = request.POST.get('primary_address')

        if not first_name:  # First name is required
            return JsonResponse({"error": "First name is required"}, status=400)

                # Use existing values if any fields are missing
        updated_data = {
            'first_name': first_name if first_name else user.first_name,
            'last_name': last_name if last_name else user.last_name,
            'profile_photo_id': profile_photo_id if profile_photo_id else user.profile_photo_id,
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
            profile_photo_id = updated_data['profile_photo_id'],
            profile_photo_url = updated_data['profile_photo_url'],
            is_verified = user.is_verified
        )


        if updated_user:
            # Manually update the fields in the user object
            for field, value in updated_data.items():
                setattr(updated_user, field, value)

            # Update the timestamp
            updated_user.updated_at = datetime.utcnow()
            updated_user.save()

            return JsonResponse({"message": "Profile updated successfully"}, status=200)

        return JsonResponse({"error": "Failed to update profile"}, status=400)
