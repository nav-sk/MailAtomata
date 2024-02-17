from django.apps import AppConfig


class EmailAutomationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "email_automation"

    def ready(self):
        from .automation.task_signal import task_signal
        from .automation.task_handler import automation_handler

        task_signal.connect(automation_handler)
