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
    primary_address: str, profile_photo_id: str, profile_photo_url: str, is_verified: str):
    user = User(
        phone=phone,
        otp=otp,
        first_name=first_name,
        last_name=last_name,
        primary_address=primary_address,
        profile_photo_id=profile_photo_id,
        profile_photo_url=profile_photo_url,
        is_verified=is_verified,
        updated_at=datetime.utcnow()
    )
    user.save()

# Function to update OTP or user details
def update_user(phone: str, otp: str, is_verified: bool = False):
    user = get_user_by_phone(phone)
    if user:
        user.otp = str(otp)
        user.is_verified = is_verified
        user.first_name = ""
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
