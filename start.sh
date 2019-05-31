#!/bin/bash

gunicorn YonionYoga.wsgi:application -c gunicorn.conf > /var/log/django/gunicorn.log 2>&1 &
