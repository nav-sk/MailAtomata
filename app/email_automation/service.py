import codecs
import csv
import re

from config.env import ENV
from django.core.files.uploadedfile import InMemoryUploadedFile

from .automation.task_signal import task_signal
from .constants import EmailStatus
from .models import Batch, Email


class ValidationService:
    @classmethod
    def validate_secret_key(cls, secret_key: str):
        print(secret_key, ENV.USER_SECRET_KEY)
        print(secret_key == ENV.USER_SECRET_KEY)
        return secret_key == ENV.USER_SECRET_KEY

    @classmethod
    def validate_csv_file(cls, csvfile: InMemoryUploadedFile):
        with csvfile.file:
            reader = csv.DictReader(codecs.iterdecode(csvfile, "utf-8"))
            headers = reader.fieldnames
            if "Email" not in headers:
                return False, "Email column is missing"
            if "Name" not in headers:
                return False, "Name column is missing"
            return True, "Valid CSV"

    @classmethod
    def validate_target(cls, target: dict):
        name = target.get("Name")
        email = target.get("Email")

        # Regex pattern for validating an email
        email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        # Regex pattern for validating a name: any word characters, hyphens or spaces
        name_regex = r"^[A-Za-z-\s]+$"

        if not name or not email:
            return False, "Name or Email is missing"
        elif not re.match(name_regex, name):
            return False, "Invalid name"
        elif not re.match(email_regex, email):
            return False, "Invalid email"
        else:
            return True, "Valid name and email"


class AutomationService:
    @classmethod
    def create_email_batch(cls, csvfile: InMemoryUploadedFile, batch_name: str):
        batch = Batch.objects.create(name=batch_name)
        email_targets_of_batch = []
        visited_emails = set()
        with csvfile.file:
            reader = csv.DictReader(codecs.iterdecode(csvfile, "utf-8"))
            for row in reader:
                if (
                    not ValidationService.validate_target(row)[0]
                    or row["Email"] in visited_emails
                ):
                    continue
                email_object = Email(batch=batch, config=row)
                email_targets_of_batch.append(email_object)
                visited_emails.add(row["Email"])

        Email.objects.bulk_create(email_targets_of_batch)

    @classmethod
    def get_batch_data(cls):
        batches = Batch.objects.prefetch_related("emails").all()
        data = []
        for batch in batches:
            batch_data = {
                "id": batch.id,
                "name": batch.name,
                "status": batch.status,
                "total_emails": batch.emails.count(),
                "completed_emails": batch.emails.filter(
                    status=EmailStatus.COMPLETED.value
                ).count(),
                "failed_emails": batch.emails.filter(
                    status=EmailStatus.FAILED.value
                ).count(),
            }
            data.append(batch_data)
        return {"batches": data}

    @classmethod
    def trigger_email_batch(cls, batch_id: str):
        batch = Batch.objects.get(id=batch_id)
        for email in batch.emails.all():
            task_signal.send(
                sender=cls.__class__, email_row_id=email.id, batch_id=batch.id
            )

    @classmethod
    def delete_batch_and_cascade_emails(cls, batch_id: str):
        batch = Batch.objects.get(id=batch_id)
        batch.delete()
