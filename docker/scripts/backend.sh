#!/bin/sh

echo "Apply database migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Starting the server..."
if [[ $ENVIRONMENT == "LOCAL" ]]; then
  python manage.py runserver 0.0.0.0:8000
else
  gunicorn config.wsgi --bind 0.0.0.0:8000 --timeout 200 --threads=3 --worker-connections=1000
fi
