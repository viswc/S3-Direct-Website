#!/bin/bash
# Navigate to the application directory and start the development server
cd /home/ec2-user/S3DirectWebsite
source venv/bin/activate
python S3DirectWebsite/manage.py migrate
python S3DirectWebsite/manage.py collectstatic --noinput
python S3DirectWebsite/manage.py runserver 0.0.0.0:8000 &
