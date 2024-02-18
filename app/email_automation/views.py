import json

from django.http import JsonResponse
from django.http.response import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.views import View
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

        result = AutomationService.create_email_batch(
            files["csvFile"], data.get("batchName")
        )
        if not result[0]:
            return render(request, "upload.html", {"error": result[1]})
        return redirect("batch_management")


class BatchManagementApiView(View):
    def get(self, request):
        data_for_frontend = AutomationService.get_batch_data()
        return render(request, "batch_manage.html", data_for_frontend)

    def post(self, request):
        data = request.body  # Used body instead of POST
        data = json.loads(data)
        if not ValidationService.validate_secret_key(data.get("secretKey")):
            return HttpResponse("Invalid Secret Key", status=403)

        batch_id = data.get("batchId")
        action = data.get("action")
        if action == "START":
            AutomationService.trigger_email_batch(batch_id)
        elif action == "DELETE":
            AutomationService.delete_batch_and_cascade_emails(batch_id)
        return redirect("batch_management")
