import mongoengine as me
from datetime import datetime
from . import user

class Address(me.Document):
    address_line1 = me.StringField()
    address_line2 = me.StringField()
    city = me.StringField()
    state = me.StringField()
    country = me.StringField()
    postal_code = me.StringField()
    user = me.ReferenceField(user.User, null=True)
    created_at = me.DateTimeField(default=datetime.utcnow)
    updated_at = me.DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'address'  # MongoDB collection name
    }