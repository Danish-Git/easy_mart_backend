import mongoengine as me
from datetime import datetime

class NewsCategories(me.Document):
    title = me.StringField(unique=True, required=True)  # Category title (e.g., Politics, Sports)
    slug = me.StringField(unique=True, required=True)  # URL-friendly identifier
    description = me.StringField()  # Short description of the category
    icon_url = me.StringField()  # URL for category icon
    cover_image = me.ReferenceField("Media", null=True)  # URL for category cover/banner image
    priority = me.IntField(default=0)  # Used for sorting categories
    status = me.BooleanField(default=True)  # Active/inactive status
    parent_category = me.ReferenceField('self', null=True)  # Parent category for subcategories
    is_featured = me.BooleanField(default=False)  # Mark as a featured category
    is_trending = me.BooleanField(default=False)  # Mark as trending
    keywords = me.ListField(me.StringField())  # List of relevant search keywords
    language = me.StringField(default="en")  # Language code (e.g., "en", "hi")
    meta_title = me.StringField()  # SEO-friendly title
    meta_description = me.StringField()  # SEO-friendly description
    created_at = me.DateTimeField(default=datetime.utcnow)  # Timestamp when created
    updated_at = me.DateTimeField(default=datetime.utcnow)  # Timestamp when last updated

    meta = {
        'collection': 'news_categories',  # MongoDB collection name
        'indexes': ['slug', 'priority', 'status', 'is_featured', 'is_trending']  # Indexed fields for performance
    }
