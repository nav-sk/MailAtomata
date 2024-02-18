import codecs
import csv
from .models import Batch, Email
from config.env import ENV
from .automation.task_signal import task_signal

from django.core.files.uploadedfile import InMemoryUploadedFile


class ValidationService:
    @classmethod
    def validate_secret_key(cls, secret_key: str):
        print(secret_key, ENV.USER_SECRET_KEY)
        print(secret_key == ENV.USER_SECRET_KEY)
        return secret_key == ENV.USER_SECRET_KEY


class AutomationService:
    @classmethod
    def create_email_batch(cls, csvfile: InMemoryUploadedFile, batch_name: str):
        batch = Batch.objects.create(name=batch_name)
        email_targets_of_batch = []
        with csvfile.file:
            reader = csv.DictReader(codecs.iterdecode(csvfile, "utf-8"))
            for row in reader:
                email_object = Email(batch=batch, config=row)
                email_targets_of_batch.append(email_object)

        Email.objects.bulk_create(email_targets_of_batch)
