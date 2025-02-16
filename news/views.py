import json
from bson import ObjectId
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core.utils import validate_jwt_token  
from core.models.news_operations import create_news, fetch_news
from core.models.user import get_user_by_id
from core.models.media_operations import get_media_by_id
from core.db_operations.collections.media_collection import Media

@method_decorator(csrf_exempt, name='dispatch')
class CreateNewsView(View):
    def post(self, request):
        """Create a new news article"""
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({"error": "Token is required"}, status = 400)

        token = token.split(' ')[1]
        user = validate_jwt_token(token)
        if not user:
            return JsonResponse({"error": "Invalid or expired token"}, status = 401)

        title = request.POST.get("title")
        if not title:
            return JsonResponse({"error": "Title is required"}, status = 400)
        
        cover_image_id = request.POST.get("cover_image")
        if not cover_image_id:
            return JsonResponse({"error": "Cover image is required"}, status = 400)
    
        try:
            news = create_news(
                posted_by = str(user.id),
                title = title,
                description = request.POST.get("description"),
                cover_image = request.POST.get("cover_image"),
                priority = request.POST.get("priority", 0),
                status = request.POST.get("status", True),
                is_featured = request.POST.get("is_featured", False),
                is_trending = request.POST.get("is_trending", False),
                keywords = request.POST.get("keywords", []),
                language = request.POST.get("language", "en"),
                category = request.POST.get("category"),
                meta_title = request.POST.get("meta_title"),
                meta_description = request.POST.get("meta_description")
            )

            # Handle posted_by if it's None
            user_data = None
            if user:
                user_data = {
                    "phone": user.phone,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "profile_photo": {
                        "image_id": str(user.profile_photo.id),
                        "category": user.profile_photo.category,
                        "image_url": user.profile_photo.image_url
                    } if user.profile_photo else None,
                    "profile_photo_url": user.profile_photo_url if user.profile_photo_url else None,
                    "primary_address": {
                        "id": str(user.primary_address.id),
                        "address_line1": user.primary_address.address_line1,
                        "address_line2": user.primary_address.address_line2,
                        "city": user.primary_address.city,
                        "state": user.primary_address.state,
                        "postal_code": user.primary_address.postal_code
                    } if user.primary_address else None,
                    "is_verified": user.is_verified,
                    "created_at": user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    "updated_at": user.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }

            # Handle cover_image if it's None
            cover_image_data = None
            if news.cover_image:
                cover_image_data = {
                    "image_id": str(news.cover_image.id),
                    "category": news.cover_image.category,
                    "image_name": news.cover_image.image_name,
                    "image_url": news.cover_image.image_url
                }

            # Handle category if it's None
            news_category = None
            if news.category:
                news_category = {
                    "id": str(news.category.id),
                    "title": news.category.title,
                    "slug": news.category.slug,
                    "description": news.category.description,
                    "icon_url": news.category.icon_url,
                    # "cover_image": news.category.cover_image,
                    "priority": news.category.priority,
                    "status": news.category.status,
                    "is_featured": news.category.is_featured,
                    "is_trending": news.category.is_trending,
                    "keywords": news.category.keywords,
                    "created_at": news.category.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    "updated_at": news.category.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }

            newsJson = None
            if news:
                newsJson = {
                    "id": str(news.id),
                    "posted_by": user_data,
                    "title": news.title,
                    "description": news.description,
                    "cover_image": cover_image_data,
                    "priority": news.priority,
                    "status": news.status,
                    "is_featured": news.is_featured,
                    "is_trending": news.is_trending,
                    "keywords": news.keywords,
                    "language": news.language,
                    "category": news_category,
                    "meta_title": news.meta_title,
                    "meta_description": news.meta_description,
                    "created_at": news.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    "uploaded_at": news.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                } 

            return JsonResponse({"message": "News created successfully", "data": newsJson}, status = 201)
                
        except ImportError as e:
            return JsonResponse({"error": "Module import error: Circular dependency detected."}, status = 500)
        except Exception as e:
            return JsonResponse({"error": "Failed to create news", "details": str(e)}, status = 500)
        




@method_decorator(csrf_exempt, name='dispatch')
class FetchNewsView(View):
    def get(self, request):
        """Fetch paginated news articles"""
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({"error": "Token is required"}, status = 400)

        token = token.split(' ')[1]
        user = validate_jwt_token(token)
        if not user:
            return JsonResponse({"error": "Invalid or expired token"}, status = 401)

        language = request.GET.get("language", "en")
        category_id = request.GET.get("category")
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 10))

        if not category_id:
            return JsonResponse({"error": "Category ID is required"}, status = 400)

        try:
            category_id = ObjectId(category_id)
        except:
            return JsonResponse({"error": "Invalid category ID"}, status = 400)

        news_list = fetch_news(language, category_id, page, page_size)

        formatted_news = []
        for news in news_list:

            # Handle posted_by if it's present
            user_data = None
            if "posted_by" in news and news["posted_by"]:
                user = get_user_by_id(news["posted_by"])
                if user:
                    user_data = {
                        "id": str(user.id),
                        "phone": user.phone,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "profile_photo": {
                            "image_id": str(user.profile_photo.id),
                            "category": user.profile_photo.category,
                            "image_url": user.profile_photo.image_url
                        } if user.profile_photo else None,
                        "profile_photo_url": user.profile_photo_url if user.profile_photo_url else None,
                        "primary_address": {
                            "id": str(user.primary_address.id),
                            "address_line1": user.primary_address.address_line1,
                            "address_line2": user.primary_address.address_line2,
                            "city": user.primary_address.city,
                            "state": user.primary_address.state,
                            "postal_code": user.primary_address.postal_code
                        } if user.primary_address else None,
                        "is_verified": user.is_verified,
                        "created_at": user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        "updated_at": user.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                    }

            # Format cover image
            cover_image_data = None
            if "cover_image" in news and news["cover_image"]:
                cover_image_obj = get_user_by_id(news["cover_image"])  # Fetch from MongoDB
                if cover_image_obj:
                    cover_image_data = {
                        "image_id": str(cover_image_obj["_id"]),
                        "category": cover_image_obj.get("category"),
                        "image_name": cover_image_obj.get("image_name"),
                        "image_url": cover_image_obj.get("image_url"),
                    }

            # Format category
            news_category = None
            if "category" in news and news["category"]:
                news_category = {
                    "id": str(news["category"]["_id"]),
                    "title": news["category"]["title"],
                    "slug": news["category"]["slug"],
                    "description": news["category"]["description"],
                    "icon_url": news["category"]["icon_url"],
                    "priority": news["category"]["priority"],
                    "status": news["category"]["status"],
                    "is_featured": news["category"]["is_featured"],
                    "is_trending": news["category"]["is_trending"],
                    "keywords": news["category"]["keywords"],
                    "created_at": news["category"]["created_at"].strftime('%Y-%m-%d %H:%M:%S'),
                    "updated_at": news["category"]["updated_at"].strftime('%Y-%m-%d %H:%M:%S')
                }

            formatted_news.append({
                "id": str(news["_id"]),
                "posted_by": user_data,
                "title": news["title"],
                "description": news["description"],
                "cover_image": cover_image_data,
                "priority": news["priority"],
                "status": news["status"],
                "is_featured": news["is_featured"],
                "is_trending": news["is_trending"],
                "keywords": news["keywords"],
                "language": news["language"],
                "category": news_category,
                "meta_title": news["meta_title"],
                "meta_description": news["meta_description"],
                "created_at": news["created_at"].strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": news["updated_at"].strftime('%Y-%m-%d %H:%M:%S')
            })

        return JsonResponse({"message": "News fetched successfully", "data": formatted_news}, status=200)
