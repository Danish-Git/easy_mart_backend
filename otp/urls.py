from django.urls import path
from . import views

urlpatterns = [
    path('send_otp/', views.SendOtpView.as_view(), name='send_otp'),
]