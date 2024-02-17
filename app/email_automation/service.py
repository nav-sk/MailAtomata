from .automation.task_signal import task_signal


class AutomationService:

    @classmethod
    def trigger_fn(cls):
        task_signal.send(sender=cls.__class__)
        print("Signal Triggered")
