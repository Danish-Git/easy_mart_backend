import mongoengine as me
from datetime import datetime

class Address(me.Document):

    @staticmethod
    def get_user_reference():
        from core.db_operations.collections.user import User  # Import inside method
        return me.ReferenceField(User, null=True)
    
    address_line1 = me.StringField()
    address_line2 = me.StringField()
    city = me.StringField()
    state = me.StringField()
    country = me.StringField()
    postal_code = me.StringField()
    # user = get_user_reference()
    user = me.ReferenceField("User", null=True)
    created_at = me.DateTimeField(default=datetime.utcnow)
    updated_at = me.DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'address'  # MongoDB collection name
    }