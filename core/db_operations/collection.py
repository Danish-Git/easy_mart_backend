import mongoengine as me
from datetime import datetime

class User(me.Document):
    phone = me.StringField(unique=True, required=True)
    otp = me.StringField()
    first_name = me.StringField(required=True)
    last_name = me.StringField()
    primary_address = me.ReferenceField('Address')  # Assuming Address model exists
    profile_photo_url = me.StringField()  # For storing profile photo URL
    created_at = me.DateTimeField(default=datetime.utcnow)
    is_verified = me.BooleanField(default=False)
    updated_at = me.DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'users'  # MongoDB collection name
    }
