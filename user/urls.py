from django.urls import path
from . import views

urlpatterns = [
    path('user/update_profile/', views.UpdateProfileView.as_view(), name='update_profile'),
]