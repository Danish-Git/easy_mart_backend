from django.urls import path
from . import views

urlpatterns = [
    path('videos/post_video/', views.CreateVideoView.as_view(), name = 'post_videos'),
    path('videos/get_videos/', views.FetchVideosView.as_view(), name='get_videos'),
]