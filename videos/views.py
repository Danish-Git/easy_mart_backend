from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from core.utils import validate_jwt_token
from core.models.videos import create_video  

@method_decorator(csrf_exempt, name='dispatch')
class CreateVideoView(View):
    def post(self, request):
        """Create a new video"""
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({"error": "Token is required"}, status=400)

        token = token.split(' ')[1]
        user = validate_jwt_token(token)
        if not user:
            return JsonResponse({"error": "Invalid or expired token"}, status=401)

        title = request.POST.get("title")
        if not title:
            return JsonResponse({"error": "Title is required"}, status=400)

        video_url = request.POST.get("video_url")
        if not video_url:
            return JsonResponse({"error": "Video URL is required"}, status=400)

        try:
            video = create_video(
                posted_by = str(user.id),
                title = title,
                description = request.POST.get("description"),
                video_url = video_url,
                cover_image = request.POST.get("cover_image"),
                priority = request.POST.get("priority", 0),
                status = request.POST.get("status", True),
                is_featured = request.POST.get("is_featured", False),
                is_trending = request.POST.get("is_trending", False),
                keywords = request.POST.getlist("keywords"),
                language = request.POST.get("language", "en"),
                category = request.POST.get("category"),
                meta_title = request.POST.get("meta_title"),
                meta_description = request.POST.get("meta_description")
            )

            # Handle user data
            user_data = {
                "phone": user.phone,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "profile_photo_url": user.profile_photo_url if user.profile_photo_url else None,
                "is_verified": user.is_verified,
                "created_at": user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": user.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }

            # Handle cover_image
            cover_image_data = None
            if video.cover_image:
                cover_image_data = {
                    "image_id": str(video.cover_image.id),
                    "image_url": video.cover_image.image_url
                }

            # Handle category
            video_category = None
            if video.category:
                video_category = {
                    "id": str(video.category.id),
                    "title": video.category.title,
                    "description": video.category.description,
                    "priority": video.category.priority,
                    "status": video.category.status,
                    "created_at": video.category.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    "updated_at": video.category.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }

            video_json = {
                "id": str(video.id),
                "posted_by": user_data,
                "title": video.title,
                "description": video.description,
                "video_url": video.video_url,
                "cover_image": cover_image_data,
                "priority": video.priority,
                "status": video.status,
                "is_featured": video.is_featured,
                "is_trending": video.is_trending,
                "keywords": video.keywords,
                "language": video.language,
                "category": video_category,
                "meta_title": video.meta_title,
                "meta_description": video.meta_description,
                "created_at": video.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "updated_at": video.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }

            return JsonResponse({"message": "Video created successfully", "data": video_json}, status=201)

        except Exception as e:
            return JsonResponse({"error": "Failed to create video", "details": str(e)}, status=500)

