#!/bin/bash

# Installing Dependencies
echo "Installing dependencies..."
pip install setuptools
pip install -r requirements.txt

# Run Django Commands
python manage.py makemigrations
python manage.py migrate
python manage.py tailwind install
python manage.py collectstatic --noinput
python manage.py tailwind build