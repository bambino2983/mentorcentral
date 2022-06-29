#!/bin/sh

python manage.py makemigrations --noinput
python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn mentorcentral.wsgi:application --bind 0.0.0.0:8000