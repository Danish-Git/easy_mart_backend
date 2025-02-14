from datetime import datetime
from core.models.news import News
from core.models.media_operations import Media
from core.models.news_categories import NewsCategories

# Function to create a new news article
def create_news(title: str, description: str = None, cover_image: str = None, priority: int = 0,
    status: bool = True, is_featured: bool = False, is_trending: bool = False, keywords: list = None,
    language: str = "en", category: str = None, meta_title: str = None, meta_description: str = None,):

    cover_image_doc = Media.objects(id=cover_image).first() if cover_image else None
    category_doc = NewsCategories.objects(id=category).first() if category else None

    news = News(
        title = title,
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
    news.save()
    return news
