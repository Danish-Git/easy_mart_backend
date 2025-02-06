from datetime import datetime
from ..db_operations.collection import User        # Import the User model

# Function to check if user exists by ID
def get_user_by_id(user_id: str):
    return User.objects(id=user_id).first()

# Function to check if user exists by phone number
def get_user_by_phone(phone_number: str):
    return User.objects(phone=phone_number).first()

# Function to save a new user
def save_user(phone: str, otp: str, first_name: str, last_name: str, 
    primary_address: str, profile_photo: str, profile_photo_url: str, is_verified: str):
    user = User(
        phon = phone,
        otp = otp,
        first_name = first_name if first_name else "",
        last_name = last_name if last_name else "",
        primary_address = primary_address if primary_address else "",
        profile_photo = profile_photo if profile_photo else "",
        profile_photo_url = profile_photo_url if profile_photo_url else "",
        is_verified = is_verified if is_verified is not None else user.is_verified,
        updated_at = datetime.utcnow()
    )
    user.save()

# Function to update OTP or user details
def update_user(phone: str, otp: str, first_name: str = None, last_name: str = None,
        primary_address: str = None, profile_photo: str = None, 
        profile_photo_url: str = None, is_verified: bool = False):
    user = get_user_by_phone(phone)
    if user:
        # Update the fields if they are not None, otherwise keep the existing value
        user.first_name = first_name if first_name else user.first_name
        user.last_name = last_name if last_name else user.last_name
        user.primary_address = primary_address if primary_address else user.primary_address
        user.profile_photo = profile_photo if profile_photo else user.profile_photo
        user.profile_photo_url = profile_photo_url if profile_photo_url else user.profile_photo_url
        user.is_verified = is_verified if is_verified is not None else user.is_verified
        user.otp = otp if otp else user.otp  # Update OTP only if a new OTP is passed
        user.updated_at = datetime.utcnow()

        user.save()
    return user

# Function to check if a phone number already exists
def phone_exists(phone: str) -> bool:
    return User.objects(phone=phone).first() is not None

# Function to get all users (if needed)
def get_all_users():
    return User.objects.all()

# Function to delete a user by phone
def delete_user(phone: str):
    user = get_user_by_phone(phone)
    if user:
        user.delete()
