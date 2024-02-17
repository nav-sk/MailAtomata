from .celery import app


@app.task(bind=True)
def automate_mail_delivery(self, *args, **kwargs):
    print(f"Automating mail delivery: {args} {kwargs}")
    print(f"Task ID: {self.request.id}")
