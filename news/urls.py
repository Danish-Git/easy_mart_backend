from django.urls import path
from . import views

urlpatterns = [
    path('news/post_news/', views.CreateNewsView.as_view(), name = 'post_news'),
    path('news/fetch_news/', views.FetchNewsView.as_view(), name = 'fetch_news'),
]