from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="email_automation"),
    path("upload/", views.CSVUploadApiView.as_view(), name="upload_csv"),
]
