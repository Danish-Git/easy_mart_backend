import mongoengine as me
from datetime import datetime

class Videos(me.Document):
    posted_by = me.ReferenceField("User", required = True)  # User who posted the video
    updated_by = me.ReferenceField("User", required = False)  # User who edited the video
    verified_by = me.ReferenceField("User", required = False)  # User who verified the video
    title = me.StringField(required = True)  # Title of the video
    description = me.StringField()  # Short description of the video
    video_url = me.StringField(required = True)  # URL of the video
    cover_image = me.ReferenceField("Media", required = False)  # Thumbnail or banner image for the video
    priority = me.IntField(default = 0)  # Used for sorting videos
    status = me.BooleanField(default = True)  # Active/inactive status
    is_featured = me.BooleanField(default = False)  # Mark as a featured video
    is_trending = me.BooleanField(default = False)  # Mark as trending
    keywords = me.ListField(me.StringField())  # List of relevant search keywords
    language = me.StringField(default = "en")  # Language code (e.g., "en", "hi")
    category = me.ReferenceField("VideoCategories", required = False)  # Category (e.g., Tutorials, Entertainment)
    meta_title = me.StringField()  # SEO-friendly title
    meta_description = me.StringField()  # SEO-friendly description
    created_at = me.DateTimeField(default = datetime.utcnow)  # Timestamp when created
    updated_at = me.DateTimeField(default = datetime.utcnow)  # Timestamp when last updated

    meta = {
        'collection': 'videos',  # MongoDB collection name
    }
