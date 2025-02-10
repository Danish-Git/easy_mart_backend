from django.urls import path
from . import views

urlpatterns = [
    path('news-categories/create/', views.CreateNewsCategories.as_view(), name='create_news_category'),
    path('news-categories/language/<str:language>/', views.NewsCategoriesByLanguageView.as_view(), name='news_categories_by_language'),
    path('news-categories/all/', views.GetNewsCategories.as_view(), name='get_all_news_categories'),
    path('news-categories/update/<str:category_id>/', views.UpdateNewsCategories.as_view(), name='update_news_category'),
    path('news-categories/delete/<str:category_id>/', views.DeleteNewsCategories.as_view(), name='delete_news_category'),
]
