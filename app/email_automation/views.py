import json
from django.shortcuts import render, redirect
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
        if not ValidationService.validate_csv_file(files["csvFile"])[0]:
            return render(
                request,
                "upload.html",
                {"error": ValidationService.validate_csv_file(files["csvFile"])[1]},
            )

        AutomationService.create_email_batch(files["csvFile"], data.get("batchName"))

        return JsonResponse({"message": "OK"})


class BatchManagementApiView(View):
    def get(self, request):
        data_for_frontend = AutomationService.get_batch_data()
        return render(request, "batch_manage.html", data_for_frontend)

    def post(self, request):
        data = request.body  # Used body instead of POST
        data = json.loads(data)
        if not ValidationService.validate_secret_key(data.get("secretKey")):
            data_for_frontend = AutomationService.get_batch_data()
            return render(
                request,
                "batch_manage.html",
                {"error": "Invalid Secret Key", **data_for_frontend},
            )

        batch_id = data.get("batchId")
        action = data.get("action")
        if action == "START":
            AutomationService.trigger_email_batch(batch_id)
        elif action == "DELETE":
            AutomationService.delete_batch_and_cascade_emails(batch_id)
        return redirect("batch_management")
