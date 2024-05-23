#!/bin/bash
# Validate that the application is running
SERVICE_STATUS=$(sudo systemctl is-active my_django_app)
if [ "$SERVICE_STATUS" = "active" ]; then
  echo "Application is running"
  exit 0
else
  echo "Application failed to start"
  exit 1
fi
