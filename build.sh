#!/usr/bin/env bash
set -e

DJANGO_SETTINGS_MODULE=config.settings.prod python manage.py collectstatic --noinput
DJANGO_SETTINGS_MODULE=config.settings.prod python manage.py migrate
