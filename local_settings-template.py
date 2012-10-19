import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
BASE_PATH = os.path.dirname(__file__)

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

INSTALLED_APPS = (
    'gunicorn',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'debug_toolbar',
    'django_bcrypt',
    'haystack',
    'markdown_deux',
    'pagination',
    'postmark',
    'registration',
    'south',
    'taggit',
    'tastypie',
    'typogrify',

    'accounts',
    'blogs',
    'snipts',
    'utils',
)

# Local time zone. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
#
# On Unix systems, a value of None will cause Django to use the same timezone as
# the operating system. On a Windows environment, this must be set to the same
# as your system time zone
TIME_ZONE = 'America/New_York'

# Language code for the Django installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_PATH, 'media/uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/uploads/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_PATH, 'static')
if DEBUG:
    STATIC_URL = '/media/'
else:
    STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_PATH, 'media'),
)

SECRET_KEY = ''

DEFAULT_FROM_EMAIL = 'support@snipt.net'
SERVER_EMAIL = 'support@snipt.net'
EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'
POSTMARK_API_KEY = ''

# Virtualenv
VIRTUALENV_PATH = ''

AMAZON_API_KEY = ''
AMAZON_API_SECRET = ''

STRIPE_API_KEY = ''

ENV_HOST = 'user@domain.com:22'

# Bugsnag
BUGSNAG = {
    "api_key": "",
    "project_root": PROJECT_PATH,
}

# HTTPS
if not DEBUG:
    USE_HTTPS = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_DOMAIN = '.snipt.net'

# Search
if not DEBUG:
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
        },
    }
else:
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    }

# Extensions
if DEBUG:
    INSTALLED_APPS += ('django_extensions',)
