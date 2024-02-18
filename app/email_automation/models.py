import uuid
from django.db import models
from .constants import BatchStatus, EmailStatus


class Batch(models.Model):
    id = models.CharField(
        max_length=100, primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=100, default=BatchStatus.PENDING.value, choices=BatchStatus.choices
    )

    def __str__(self):
        return f"< {self.name} : {self.id}>"


class Email(models.Model):
    id = models.CharField(
        max_length=100, primary_key=True, default=uuid.uuid4, editable=False
    )
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="emails")
    config = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=100, default=EmailStatus.PENDING.value, choices=EmailStatus.choices
    )

    def __str__(self):
        return f"< {self.batch.name} : {self.id}>"
