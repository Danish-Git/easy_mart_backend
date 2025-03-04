import mongoengine as me
from datetime import datetime

class Media(me.Document):
    category = me.StringField(required=True)
    image_name = me.StringField()
    image_url = me.StringField(required=True)
    user = me.ReferenceField("User", null=True)
    updated_at = me.DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'media'  # MongoDB collection name
    }   