import mongoengine as me
from datetime import datetime

class News(me.Document):
    posted_by = me.ReferenceField("User", required = True)  # User for recognisation who posted news
    updated_by = me.ReferenceField("User", required = False)  # User for recognisation who edited news
    verified_by = me.ReferenceField("User", required = False)  # User for recognisation who verified news
    title = me.StringField(required = True)  # Title (e.g., Politics, Sports)
    description = me.StringField()  # Short description of the category
    cover_image = me.ReferenceField("Media", required = False)  # URL for category cover/banner image
    priority = me.IntField(default = 0)  # Used for sorting categories
    status = me.BooleanField(default = True)  # Active/inactive status
    is_featured = me.BooleanField(default = False)  # Mark as a featured category
    is_trending = me.BooleanField(default = False)  # Mark as trending
    keywords = me.ListField(me.StringField())  # List of relevant search keywords
    language = me.StringField(default = "en")  # Language code (e.g., "en", "hi")
    category = me.ReferenceField("NewsCategories", required = False)  # Category (e.g., Politics, Sports)
    meta_title = me.StringField()  # SEO-friendly title
    meta_description = me.StringField()  # SEO-friendly description
    created_at = me.DateTimeField(default = datetime.utcnow)  # Timestamp when created
    updated_at = me.DateTimeField(default = datetime.utcnow)  # Timestamp when last updated

    meta = {
        'collection': 'news',  # MongoDB collection name
    }
