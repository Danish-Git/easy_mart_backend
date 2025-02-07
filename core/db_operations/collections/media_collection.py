import mongoengine as me
from datetime import datetime
from .user import User

class Media(me.Document):
    category = me.StringField(unique=True, required=True)
    image_name = me.StringField()
    image_url = me.StringField(required=True)
    user = me.ReferenceField("User", null=True)
    updated_at = me.DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'media'  # MongoDB collection name
    }   