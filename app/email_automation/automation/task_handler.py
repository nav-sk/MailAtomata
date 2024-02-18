from core.tasks import automate_mail_delivery
from django.dispatch import receiver
from .task_signal import task_signal


@receiver(task_signal, weak=False)
def automation_handler(*args, **kwargs):
    print("handling")
    print(*args, **kwargs)
    automate_mail_delivery.delay("HI")
    print("Handled!")
