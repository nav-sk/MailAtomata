from django.dispatch import Signal

# Enabling Signals based message passing
# task_signal = Signal(providing_args=["event_id", "event_type", "params"])

task_signal = Signal()
