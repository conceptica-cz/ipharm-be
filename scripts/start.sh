#!/bin/bash

./scripts/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT

python manage.py migrate
python manage.py runserver 0.0.0.0:8000