from datetime import datetime
from core.db_operations.collections.news_categories import NewsCategories
from ..db_operations.collections.media_collection import Media

# Function to get a news category by ID
def get_news_category_by_id(category_id: str):
    return NewsCategories.objects(id=category_id).first()

# Function to get a category by slug
def get_news_category_by_slug(slug: str):
    return NewsCategories.objects(slug=slug).first()

# Function to create a new news category
def create_news_category(title: str, slug: str, description: str = None, icon_url: str = None,
    cover_image: str = None, priority: int = 0, status: bool = True,
    parent_category: str = None, is_featured: bool = False, is_trending: bool = False,
    keywords: list = None, language: str = "en", meta_title: str = None,
    meta_description: str = None):
    
    # if get_news_category_by_slug(slug):
    #     return None  # Slug must be unique
    
    parent = get_news_category_by_id(parent_category) if parent_category else None
    
    category = NewsCategories(
        title = title,
        slug = slug,
        description = description,
        icon_url = icon_url,
        cover_image = cover_image,
        priority = priority,
        status = status,
        parent_category = parent,
        is_featured = is_featured,
        is_trending = is_trending,
        keywords = keywords or [],
        language = language,
        meta_title = meta_title,
        meta_description = meta_description,
        created_at = datetime.utcnow(),
        updated_at = datetime.utcnow()
    )
    category.save()
    return category

# Function to update an existing news category
def update_news_category(category_id: str, title: str = None, slug: str = None, description: str = None,
    icon_url: str = None, cover_image: str = None, priority: int = None, status: bool = True,
    parent_category: str = None, is_featured: bool = None, is_trending: bool = None,
    keywords: list = None, language: str = None, meta_title: str = None,
    meta_description: str = None):

    category = get_news_category_by_id(category_id)
    if not category:
        print(f"Category with ID {category_id} not found!")  # Debugging
        return None

    category.title = title if title else category.title
    category.slug = slug if slug else category.slug
    category.description = description if description else category.description
    category.icon_url = icon_url if icon_url else category.icon_url
    category.priority = int(priority) if priority is not None else category.priority
    category.status = bool(status) if status is not None else category.status
    category.is_featured = bool(is_featured) if is_featured is not None else category.is_featured
    category.is_trending = bool(is_trending) if is_trending is not None else category.is_trending
    category.keywords = keywords if keywords else category.keywords
    category.language = language if language else category.language
    category.meta_title = meta_title if meta_title else category.meta_title
    category.meta_description = meta_description if meta_description else category.meta_description
    category.updated_at = datetime.utcnow()

    if parent_category:
        parent = get_news_category_by_id(parent_category)
        if parent:
            category.parent_category = parent
        else:
            print(f"Parent category {parent_category} not found!")  # Debugging

    if cover_image:
        media = Media.objects(id = cover_image).first()
        if media:
            category.cover_image = media
        else:
            print(f"Media with ID {cover_image} not found!")

    try:
        category.save()
        print("Category updated successfully!")  # Debugging
        return category
    except Exception as e:
        print(f"Error saving category: {e}")
        return None


# Function to get all news categories
def get_all_news_categories():
    return NewsCategories.objects.all()


# Fetch categories based on the selected language
def get_news_categories_by_language(language: str):
    categories = NewsCategories.objects.aggregate([
        {
            "$match": { 
                "language": language, 
                "status": True 
            }
        },
        {
            "$addFields": { 
                "is_featured_first": { 
                    "$cond": { "if": { "$eq": ["$title", "Feature"] }, "then": 1, "else": 0 } 
                }
            }
        },
        {
            "$sort": { 
                "is_featured_first": -1,  # "Feature" category always first
                "is_trending": -1,        # Trending categories first
                "priority": 1             # Lower priority value means higher importance
            }
        }
    ])
    return categories

# Function to delete a news category by ID
def delete_news_category(category_id: str):
    category = get_news_category_by_id(category_id)
    if category:
        category.delete()
        return True
    return False
