import mongoengine as me
from datetime import datetime

class Address(me.Document):
    address_line1 = me.StringField()
    address_line2 = me.StringField()
    city = me.StringField()
    state = me.StringField()
    country = me.StringField()
    postal_code = me.StringField()

    meta = {
        'collection': 'address'  # MongoDB collection name
    } 

class Media(me.Document):
    category = me.StringField(unique=True, required=True)
    image_name = me.StringField()
    image_url = me.StringField(required=True)
    updated_at = me.DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'media'  # MongoDB collection name
    }       

class User(me.Document):
    phone = me.StringField(unique=True, required=True)
    otp = me.StringField()
    first_name = me.StringField(required=True)
    last_name = me.StringField()
    primary_address = me.ReferenceField(Address)  # Assuming Address model exists
    profile_photo = me.StringField(Media)  # For storing profile photo ID
    profile_photo_url = me.StringField()  # For storing profile photo URL
    created_at = me.DateTimeField(default=datetime.utcnow)
    is_verified = me.BooleanField(default=False)
    updated_at = me.DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'users'  # MongoDB collection name
    }    
