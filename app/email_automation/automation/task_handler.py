from core.tasks import automate_mail_delivery
from django.dispatch import receiver

from .task_signal import task_signal


@receiver(task_signal, weak=False)
def automation_handler(*args, **kwargs):
    batch_id = kwargs.get("batch_id")
    automate_mail_delivery.delay(batch_id=batch_id)
    print("Task signal received and task is scheduled for batch_id: ", batch_id)
