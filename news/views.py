import json
from bson import ObjectId
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core.utils import validate_jwt_token  
from core.models.news_operations import create_news

@method_decorator(csrf_exempt, name='dispatch')
class CreateNewsView(View):
    def post(self, request):
        # from core.models.news import create_news  # Import inside function to avoid circular import
        """Create a new news article"""
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({"error": "Token is required"}, status = 400)

        token = token.split(' ')[1]
        user_data = validate_jwt_token(token)
        if not user_data:
            return JsonResponse({"error": "Invalid or expired token"}, status = 401)
        
        try:
            data = json.loads(request.body.decode("utf-8"))  # Properly parse JSON
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        title = data.get("title")
        if not title:
            return JsonResponse({"error": "Title is required"}, status=400)

        try:
            news = create_news(
                posted_by = str(user_data.id),
                title = title,
                description = data.get("description"),
                cover_image = data.get("cover_image"),
                priority = data.get("priority", 0),
                status = data.get("status", True),
                is_featured = data.get("is_featured", False),
                is_trending = data.get("is_trending", False),
                keywords = data.get("keywords", []),
                language = data.get("language", "en"),
                category = data.get("category"),
                meta_title = data.get("meta_title"),
                meta_description = data.get("meta_description")
            )

            # Handle cover_image if it's None
            cover_image_data = None
            if news.cover_image:
                cover_image_data = {
                    "image_id": str(news.cover_image.id),
                    "category": news.cover_image.category,
                    "image_name": news.cover_image.image_name,
                    "image_url": news.cover_image.image_url
                }

            return JsonResponse({
                "message": "News created successfully", 
                "data": {
                    "id": str(news.id),
                    "posted_by": str(news.posted_by.id),
                    "title": news.title,
                    "description": news.description,
                    "cover_image": cover_image_data,
                    "priority": news.priority,
                    "status": news.status,
                    "is_featured": news.is_featured,
                    "is_trending": news.is_trending,
                    "keywords": news.keywords,
                    "language": news.language,
                    "category": news.category,
                    "meta_title": news.meta_title,
                    "meta_description": news.meta_description,
                    "created_at": news.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    "uploaded_at": news.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }, status = 201)
                
        except ImportError as e:
            return JsonResponse({"error": "Module import error: Circular dependency detected."}, status = 500)
        except Exception as e:
            return JsonResponse({"error": "Failed to create news", "details": str(e)}, status = 500)
        


