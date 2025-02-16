import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from core.models.news_categories import create_news_category, update_news_category, delete_news_category, get_news_categories_by_language
from core.db_operations.collections.news_categories import NewsCategories
from core.utils import validate_jwt_token

@method_decorator(csrf_exempt, name='dispatch')
class CreateNewsCategories(View):
    def post(self, request):
        """ Create a new news category """
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({"error": "Token is required"}, status=400)

        token = token.split(' ')[1]
        user_data = validate_jwt_token(token)
        if not user_data:
            return JsonResponse({"error": "Invalid or expired token"}, status=401)

        title = request.POST.get("title")
        slug = request.POST.get("slug")
        description = request.POST.get("description", "")
        icon_url = request.POST.get("icon_url", "")
        cover_image = request.POST.get("cover_image", "")
        priority = request.POST.get("priority", 0)
        status = request.POST.get("status", True)
        language = request.POST.get("language", "en")
        is_featured = request.POST.get("is_featured", False)
        is_trending = request.POST.get("is_trending", False)
        keywords = request.POST.getlist("keywords")

        if not title or not slug:
            return JsonResponse({"error": "Title and Slug are required"}, status=400)

        category = create_news_category(
            title = title,
            slug = slug,
            description = description,
            icon_url = icon_url,
            cover_image = cover_image,
            priority = priority,
            status = status,
            language = language,
            is_featured = is_featured,
            is_trending = is_trending,
            keywords = keywords,
        )

        return JsonResponse({"message": "News category created successfully", "data": category}, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class UpdateNewsCategories(View):
    def put(self, request, category_id):
        """ Update an existing news category """
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({"error": "Token is required"}, status=400)

        token = token.split(' ')[1]
        user_data = validate_jwt_token(token)
        if not user_data:
            return JsonResponse({"error": "Invalid or expired token"}, status=401)

        
        category = update_news_category(
            category_id = category_id,
            title = request.POST.get("title"), 
            slug =request.POST.get("slug"),
            description = request.POST.get("description"),
            icon_url = request.POST.get("icon_url"),
            cover_image = request.POST.get("cover_image"),
            priority = request.POST.get("priority"),
            status = bool(request.POST.get("status")),
            is_featured = request.POST.get("is_featured"),
            is_trending = request.POST.get("is_trending"),
            keywords = request.POST.getlist("keywords"),
        )

        return JsonResponse({"message": "News category updated successfully", "data": json.loads(category.to_json())}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class DeleteNewsCategories(View):
    def delete(self, request):
        """ Delete a news category """
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({"error": "Token is required"}, status=400)

        token = token.split(' ')[1]
        user_data = validate_jwt_token(token)
        if not user_data:
            return JsonResponse({"error": "Invalid or expired token"}, status=401)

        category_id = request.POST.get("category_id")

        category = delete_news_category(category_id)
        if not category:
            return JsonResponse({"error": "Category not found"}, status=404)

        return JsonResponse({"message": "News category deleted successfully"}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class GetNewsCategories(View):
    def get(self, request):
        """ Get all categories or a single category by ID """
        category_id = request.GET.get("category_id")

        if category_id:
            category = NewsCategories.objects(id=category_id).first()
            if not category:
                return JsonResponse({"error": "Category not found"}, status=404)
            
            category_data = {
                "id": str(category.id),
                "title": category.title,
                "slug": category.slug,
                "description": category.description,
                "icon_url": category.icon_url,
                "cover_image": category.cover_image,
                "priority": category.priority,
                "status": category.status,
                "is_featured": category.is_featured,
                "is_trending": category.is_trending,
                "keywords": category.keywords,
                "created_at": category.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": category.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            return JsonResponse({"message": "Category found", "data": category_data}, status=200)

        # Get all categories
        categories = NewsCategories.objects.all()
        categories_data = [
            {
                "id": str(cat.id),
                "title": cat.title,
                "slug": cat.slug,
                "description": cat.description,
                "icon_url": cat.icon_url,
                "cover_image": cat.cover_image,
                "priority": cat.priority,
                "status": cat.status,
                "is_featured": cat.is_featured,
                "is_trending": cat.is_trending,
                "keywords": cat.keywords,
                "created_at": cat.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": cat.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for cat in categories
        ]

        return JsonResponse({"message": "All categories retrieved successfully", "data": categories_data}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class NewsCategoriesByLanguageView(View):
    def get(self, request, language):

        """ Get all categories or a single category by ID """
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({"error": "Token is required"}, status=400)

        token = token.split(' ')[1]
        user_data = validate_jwt_token(token)
        if not user_data:
            return JsonResponse({"error": "Invalid or expired token"}, status=401)

        # Fetch categories based on the selected language
        categories = get_news_categories_by_language(language)

        # Convert categories to JSON response
        category_list = []
        for category in categories:
            category_list.append({
                "id": str(category.id),
                "title": category.title,
                "slug": category.slug,
                "description": category.description,
                "icon_url": category.icon_url,
                # "cover_image": str(category.cover_image.id) if category.cover_image else None,
                "priority": category.priority,
                "is_featured": category.is_featured,
                "is_trending": category.is_trending,
                "keywords": category.keywords,
                "meta_title": category.meta_title,
                "meta_description": category.meta_description,
                "created_at": category.created_at.isoformat(),
                "updated_at": category.updated_at.isoformat(),
            })

        return JsonResponse({"categories": category_list}, status=200)