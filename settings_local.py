import os
from settings import INSTALLED_APPS

DEBUG = True

TEMPLATE_DEBUG = DEBUG

BASE_PATH = os.path.dirname(__file__)

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    ('Nick Sergeant', 'nick@snipt.net'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'snipt',
        'USER': 'Nick',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

TIME_ZONE = 'America/New_York'

LANGUAGE_CODE = 'en-us'

MEDIA_ROOT = os.path.join(BASE_PATH, 'media/uploads')

MEDIA_URL = '/media/uploads/'

STATIC_URL = '/media/'

SECRET_KEY = 'afk&6t4l#x+9hhhpl2&3zm&me06fcu&v3*j54kxitbe8kg-19)'

DEFAULT_FROM_EMAIL = 'support@snipt.net'
SERVER_EMAIL = 'support@snipt.net'
EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'
POSTMARK_API_KEY = 'c7a956a8-ac57-4bce-b5fe-b43217d0ee1b'

VIRTUALENV_PATH = '/Users/Nick/.virtualenvs/snipt/lib/python2.7/site-packages/'

AMAZON_API_KEY = 'AKIAJJRRQPTSPKB7GYOA'
AMAZON_API_SECRET = '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'

STRIPE_API_KEY = '5XchbRsWVbksTRWSX67kOdBnCf01DxSh'

ENV_HOST = 'nick@snipt.net:40030'

USE_HTTPS = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_DOMAIN = '*.snipt.localhost'
ALLOWED_HOSTS = ['*']

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}

INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
    'raven.contrib.django.raven_compat',
)

RAVEN_CONFIG = {
    'dsn': 'https://61ba6cc5b9c341e6984b8018658f725f:a2a5cdd17f7047b593f40e43b8b073af@app.getsentry.com/6849',
}
