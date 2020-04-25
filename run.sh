#!/usr/bin/env bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
# gunicorn test_task.wsgi:application --workers=3 --bind='0.0.0.0:8000' - for production