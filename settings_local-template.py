import os
from settings import INSTALLED_APPS, MIDDLEWARE_CLASSES

DEBUG = True

TEMPLATE_DEBUG = DEBUG

BASE_PATH = os.path.dirname(__file__)

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    ('Name', 'name@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'snipt',
        'USER': '',
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

SECRET_KEY = ''

DEFAULT_FROM_EMAIL = 'support@snipt.net'
SERVER_EMAIL = 'support@snipt.net'
EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'
POSTMARK_API_KEY = ''

VIRTUALENV_PATH = ''

AMAZON_API_KEY = ''
AMAZON_API_SECRET = ''

STRIPE_SECRET_KEY = ''

ENV_HOST = 'user@domain.com:22'

USE_HTTPS = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_DOMAIN = '.snipt.net'
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
    'dsn': '',
}

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
  'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
)

INTERCOM_SECRET_KEY = ''
