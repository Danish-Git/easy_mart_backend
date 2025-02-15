import json
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

        title = request.POST.get("title")
        print(title)
        
        if not title:
            return JsonResponse({"error": "Title is required"}, status=400)

        try:
            news = create_news(
                posted_by = str(user_data.id),
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
            if news:
                return JsonResponse({"message": "News created successfully", "data": news}, status = 201)
        except ImportError as e:
            return JsonResponse({"error": "Module import error: Circular dependency detected."}, status = 500)
        except Exception as e:
            return JsonResponse({"error": "Failed to create news", "details": str(e)}, status = 500)
        


