#!/bin/bash

./scripts/wait-for-it.sh app:8000
python manage.py test