#!/usr/bin/env bash

set -o errexit

poetry install
#python manage.py collectstatic --no-input
python manage.py migrate
python manage.py loaddata companies
python manage.py loaddata jobs