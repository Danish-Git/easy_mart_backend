from django.http import JsonResponse
from django.views import View

class SendOtpView(View):
    def get(self, request):
        return JsonResponse({"message": "Hello World"})