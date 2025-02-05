from django.urls import path
# from . import views
from .views import SendOtpView

urlpatterns = [
    # path('send_otp/', views.SendOtpView.as_view(), name='send_otp'),
    path('api/v1/send_otp/', SendOtpView.as_view(), name='send_otp'),
]