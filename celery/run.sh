#!/bin/sh

set -x
set -e

python manage.py collectstatic --noinput
python -m celery -A core worker --loglevel=INFO --concurrency=10 -n worker1@%h
