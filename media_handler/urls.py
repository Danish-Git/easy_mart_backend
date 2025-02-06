from django.urls import path
from . import views

urlpatterns = [
    path('upload-photo/', views.ImageUploadView.as_view(), name='upload_media'),
]