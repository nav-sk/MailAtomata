#!/bin/sh

set -x
set -e

#python manage.py wait_for_db
python manage.py collectstatic --noinput

python manage.py migrate

gunicorn config.wsgi:application --bind 0.0.0.0:9000 --workers 6 --log-level=debug
