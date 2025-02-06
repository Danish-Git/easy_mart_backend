import os
from datetime import datetime
from django.conf import settings
import mongoengine as me
from ..db_operations.collection import Media        # Import the Media model


# Function to save media record
def save_media(category: str, image_name: str):
    image_url = os.path.join(settings.MEDIA_URL, category, image_name)
    
    media_entry = Media(
        category=category,
        image_name=image_name,
        image_url=image_url,
        updated_at=datetime.utcnow()
    )
    media_entry.save()
    return media_entry

# Function to get media by category
def get_media_by_category(category: str):
    return Media.objects(category=category).all()

# Function to get media by ID
def get_media_by_id(media_id: str):
    try:
        return Media.objects.get(id=media_id)
    except me.DoesNotExist:
        return None

# Function to delete a media entry
def delete_media(image_name: str):
    media = Media.objects(image_name=image_name).first()
    if media:
        media.delete()
        return True
    return False
