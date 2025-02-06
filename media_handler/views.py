import os
import time
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings 
from core.utils import upload_photo_by_category
from core.models.media_operations import save_media


# Define the base directory for uploads
UPLOAD_BASE_DIR = settings.MEDIA_ROOT

@method_decorator(csrf_exempt, name='dispatch')
class ImageUploadView(View):
    def post(self, request):
        # Get the category and image from the request
        category = request.POST.get('category')
        image = request.FILES.get('image')

        if not category:
            return JsonResponse({"error": "Category is required"}, status=400)
        
        if category not in settings.ALLOWED_CATEGORIES:
            return JsonResponse({"error": "Invalid category"}, status=400)
        
        if not image:
            return JsonResponse({"error": "Image file is required"}, status=400)

        try:
            # Upload the photo using helper function
            image_url, image_name = upload_photo_by_category(image, category)

            # Save image details in MongoDB
            media_entry = save_media(category, image_name)

            # Return success response
            return JsonResponse({
                "message": "Image uploaded successfully",
                "data": {
                    "image_id": str(media_entry.id),
                    "category": media_entry.category,
                    "image_name": media_entry.image_name,
                    "image_url": media_entry.image_url,
                    "uploaded_at": media_entry.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            })
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Internal Server Error"}, status=500)
