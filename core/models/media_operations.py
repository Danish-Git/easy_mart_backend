import os
from datetime import datetime
from django.conf import settings
import mongoengine as me
from ..db_operations.collections.media_collection import Media

# Function to save media record
def save_media(category: str, image_name: str, user: None):
    image_url = os.path.join(settings.MEDIA_URL, category, image_name)
    
    # Ensure user is valid and get the user ID
    user_id = user.id if user else None

    # Check if user already has a profile image
    if category == "profile" and user_id:
        existing_media = Media.objects(category = "profile", user = user_id).first()
        if existing_media:
            # Get old image path from existing media
            old_image_path = os.path.join(settings.MEDIA_ROOT, existing_media.image_url.lstrip('/'))

            # Delete old image from storage if it exists
            if os.path.exists(old_image_path):
                os.remove(old_image_path)

            # Remove old entry from DB
            existing_media.delete()

    media_entry = Media(
        category = category,
        image_name = image_name,
        image_url = image_url,
        user = user,
        updated_at = datetime.utcnow()
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
