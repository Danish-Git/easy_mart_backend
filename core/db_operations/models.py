import mongoengine as me
from datetime import datetime

class User(me.Document):
    phone = me.StringField(unique=True, required=True)
    otp = me.StringField(required=True)
    created_at = me.DateTimeField(default=datetime.utcnow)  # Timestamp when OTP is created
    is_verified = me.BooleanField(default=False)  # Flag for OTP verification
    updated_at = me.DateTimeField(default=datetime.utcnow)  # Timestamp for last update

    meta = {
        'collection': 'users'  # MongoDB collection name
    }
