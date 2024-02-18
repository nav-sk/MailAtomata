from django.shortcuts import render
from django.http import JsonResponse

from django.views import View
from django.http.request import HttpRequest
from .service import AutomationService, ValidationService


def index(request):
    AutomationService.trigger_fn()
    return JsonResponse({"message": "Hello, World!"})


class CSVUploadApiView(View):

    def get(self, request):
        return render(request, "upload.html")

    def post(self, request: HttpRequest):
        data = request.POST
        files = request.FILES

        if files.get("csvFile") is None:
            return render(request, "upload.html", {"error": "No file found"})

        if not ValidationService.validate_secret_key(data.get("secretKey")):

            return render(request, "upload.html", {"error": "Invalid Secret Key"})

        AutomationService.create_email_batch(files["csvFile"], data.get("batchName"))

        return JsonResponse({"message": "OK"})
