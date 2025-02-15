import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core.utils import validate_jwt_token  
from core.models.news_operations import News

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
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status = 400)

        try:
            news = News.create_news(
                title = data.get("title"),
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
            if news:
                return JsonResponse({"message": "News created successfully", "data": news}, status = 201)
        except ImportError as e:
            return JsonResponse({"error": "Module import error: Circular dependency detected."}, status = 500)
        except Exception as e:
            return JsonResponse({"error": "Failed to create news", "details": str(e)}, status = 500)
        


