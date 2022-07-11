#!/bin/bash

./scripts/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT

python manage.py migrate
python manage.py collectstatic --noinput
gunicorn ipharm_web.wsgi:application --reload --bind 0.0.0.0:8000