from datetime import datetime
from bson.objectid import ObjectId
from core.db_operations.collections.news import News
from core.db_operations.collections.media_collection import Media
from core.db_operations.collections.news_categories import NewsCategories
from core.models.user import get_user_by_id

# Function to create a new news article
def create_news(posted_by: str, title: str, description: str = None, cover_image: str = None, priority: int = 0,
    status: bool = True, is_featured: bool = False, is_trending: bool = False, keywords: list = None,
    language: str = "en", category: str = None, meta_title: str = None, meta_description: str = None,):

    user = get_user_by_id(posted_by)
    cover_image_doc = None
    if cover_image: 
        cover_image_temp = Media.objects(id = ObjectId(cover_image)).first() 
        if cover_image_temp:
            cover_image_doc = cover_image_temp
        else:
            cover_image_doc = None

    category_doc = None
    if category:
        category_doc_temp = NewsCategories.objects(id = category).first()
        if category_doc_temp:
            category_doc = category_doc_temp
        else:
            category_doc = None

    news = News(
        posted_by = user,
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


# Function to fetch paginated news
def fetch_news(language: str, category_id: ObjectId, page: int, page_size: int):
    skip = (page - 1) * page_size

    pipeline = [
        {"$match": {"language": language, "category": category_id, "status": True}},
        {"$sort": {"_id": -1}},  # Sort by most recent first
        {"$skip": skip},         # Skip documents for pagination
        {"$limit": page_size}    # Limit results per page
    ]

    return list(News.objects.aggregate(pipeline)) 

# Function to fetch counts of all news
def fetch_news_count(language, category_id):
    """Returns the total count of news articles for the given language and category."""
    query = {
        "language": language,
        "category": category_id  # Assuming category is stored as an ObjectId
    }
    return News.objects.filter(language = language, category = category_id).count()


# Function to fetch paginated trending news
def fetch_trending_news(language: str, category_id: ObjectId, page: int, page_size: int):
    skip = (page - 1) * page_size

    pipeline = [
        {"$match": {"language": language, "category": category_id, "status": True, "is_trending": True}},
        {"$sort": {"_id": -1}},  # Sort by most recent first
        {"$skip": skip},          # Skip documents for pagination
        {"$limit": page_size}     # Limit results per page
    ]

    return list(News.objects.aggregate(pipeline))

# Function to fetch counts of all trending news
def fetch_trending_news_count(language, category_id):
    """Returns the total count of trending news articles for the given language and category."""
    return News.objects.filter(language=language, category=category_id, status=True, is_trending=True).count()
