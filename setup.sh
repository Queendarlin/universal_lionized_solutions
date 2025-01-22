#!/bin/bash

# Installing Dependencies
echo "Installing dependencies..."
pip install setuptools
pip install -r requirements.txt

# Run Django Commands
python manage.py makemigrations
python manage.py migrate

# Tailwind setup and build
python manage.py tailwind init
python manage.py tailwind install

python manage.py tailwind build

# Collect static files
python manage.py collectstatic --noinput

