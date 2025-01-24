#!/bin/sh
/usr/local/bin/python manage.py makemigrations orders
python manage.py migrate
python manage.py runserver 0.0.0.0:8000