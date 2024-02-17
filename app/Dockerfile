FROM python:3.12

ENV PYTHONBUFFERED 1

COPY requirements.txt ./
COPY app/run.sh /scripts/
COPY app /app

WORKDIR /app
EXPOSE 9000

RUN pip install --no-cache-dir -r /requirements.txt \
    && adduser \
    --disabled-password \
    --no-create-home \
    django-user \
    && chmod -R 755 /app \
    && chmod -R +x /scripts/ \
    && chown -R django-user:django-user /app

ENV PATH="/scripts:$PATH"

USER django-user

CMD ["run.sh"]
