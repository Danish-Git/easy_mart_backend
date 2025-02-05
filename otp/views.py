from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class SendOtpView(View):
    def get(self, request):
        return JsonResponse({"message": "Hello World from GET"})

    def post(self, request):
        return JsonResponse({"message": "Hello World from POST"})
