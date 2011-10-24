#!/usr/bin/env bash

gunicorn_django snipt/settings.py -c gunicorn.conf.py debug_wsgi:application
