from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from email_automation.constants import EMAIL_SUBJECT, BatchStatus, EmailStatus
from email_automation.models import Batch, Email

from .celery import app


@app.task(bind=True)
def automate_mail_delivery(self, *args, **kwargs):
    print("-" * 50)
    print(f"Automating mail delivery: {kwargs}")
    print(f"Task ID: {self.request.id}")
    batch_id = kwargs.get("batch_id")
    for email_target in Email.objects.filter(
        batch_id=batch_id, status=EmailStatus.PENDING.value
    ):
        send_email_to_target.delay(email_target_id=email_target.id)
        email_target.status = EmailStatus.IN_PROGRESS.value
        email_target.save()
    Batch.objects.filter(id=batch_id).update(status=BatchStatus.IN_PROGRESS.value)
    print(f"Task {self.request.id} completed for batch {batch_id}")
    print("-" * 50)


@app.task(bind=True)
def send_email_to_target(self, *args, **kwargs):
    print("-" * 50)
    print(f"Sending email to target: {kwargs}")
    print(f"Task ID: {self.request.id}")
    email_target_id = kwargs.get("email_target_id")
    email_target = Email.objects.get(id=email_target_id)
    # Send email to target

    email = EmailMessage(
        subject=EMAIL_SUBJECT,
        body=render_to_string(
            "email_template.html",
            {
                "name": email_target.config.get("Name"),
            },
        ),
        to=[email_target.config.get("Email")],
    )
    email.content_subtype = "html"
    email.from_email = "Hecker <Naveen SK>"
    email.send()
    email_target.status = EmailStatus.COMPLETED.value
    email_target.save()

    print(f"Task {self.request.id} completed for {email_target.config.get('Email')}")
    print("-" * 50)
