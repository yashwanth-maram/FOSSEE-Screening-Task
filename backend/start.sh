#!/usr/bin/env bash

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

# Create demo user if it doesn't exist
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='demo').exists():
    User.objects.create_user('demo', 'demo@example.com', 'demo1234')
    print('Demo user created')
else:
    print('Demo user already exists')
"

# Start Gunicorn server
gunicorn config.wsgi:application --bind 0.0.0.0:10000
