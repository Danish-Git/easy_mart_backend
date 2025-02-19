from datetime import datetime
from bson import ObjectId
from core.models.user import get_user_by_id
from core.models.media_operations import get_media_by_id

# Function to create a new video
def create_video(posted_by: str, title: str, video_url: str, description: str = None, cover_image: str = None, 
    priority: int = 0, status: bool = True, is_featured: bool = False, is_trending: bool = False, keywords: list = None, 
    language: str = "en", category: str = None, meta_title: str = None, meta_description: str = None):

    user = get_user_by_id(posted_by)
    
    cover_image_doc = None
    if cover_image:
        cover_image_temp = get_media_by_id(cover_image)
        if cover_image_temp:
            cover_image_doc = cover_image_temp

    category_doc = None
    # if category:
    #     category_doc_temp = VideoCategories.objects(id=ObjectId(category)).first()
    #     if category_doc_temp:
    #         category_doc = category_doc_temp

    video = Video(
        posted_by = user,
        title = title,
        video_url = video_url,
        description = description,
        cover_image = cover_image_doc,
        priority = priority,
        status = status,
        is_featured = is_featured,
        is_trending = is_trending,
        keywords = keywords or [],
        language = language,
        category = category_doc,
        meta_title = meta_title,
        meta_description = meta_description,
        created_at = datetime.utcnow(),
        updated_at = datetime.utcnow(),
    )
    video.save()
    return video
