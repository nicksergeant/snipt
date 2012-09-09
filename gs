#!/usr/local/bin/fish

gunicorn -c gunicorn.conf.py debug_wsgi:application
