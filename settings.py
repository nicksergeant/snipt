# Django settings for sidepros project.

import os, socket

if socket.gethostname() in ['nickmba.local', 'nickimac.local']:
    DEBUG = True
else:
    DEBUG = False
TEMPLATE_DEBUG = DEBUG
BASE_PATH = os.path.dirname(__file__)

ADMINS = (
    ('Nick Sergeant', 'nick@snipt.net'),
)
MANAGERS = ADMINS

INTERNAL_IPS = ('127.0.0.1',)

if DEBUG:
    DB_USER = 'Nick'
else:
    DB_USER = 'nick'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'snipt',
        'USER': DB_USER,
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

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

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'afk&6t4l#x+9hhhpl2&3zm&me06fcu&v3*j54kxitbe8kg-19)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'blogs.middleware.BlogMiddleware',
)

ROOT_URLCONF = 'snipt.urls'

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates')
)

INSTALLED_APPS = (
    'gunicorn',
    #'grappelli',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'django_bcrypt',
    'haystack',
    'markdown_deux',
    'pagination',
    'postmark',
    'registration',
    'south',
    'taggit',
    'tastypie',

    'blogs',
    'snipts',
    'utils',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Email
DEFAULT_FROM_EMAIL = 'site@snipt.net'
SERVER_EMAIL = 'site@snipt.net'
EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'
POSTMARK_API_KEY = '608d3101-1706-4a96-819f-f2f36fe00fe0'

# Grappelli settings
GRAPPELLI_ADMIN_TITLE = '<a href="/">Snipt</a>'

# Virtualenv
if DEBUG:
    VIRTUALENV_PATH = '/Users/Nick/.virtualenvs/snipt/lib/python2.7/site-packages/'
else:
    VIRTUALENV_PATH = '/home/nick/.virtualenvs/snipt/lib/python2.7/site-packages/'

# Account settings
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
ACCOUNT_ACTIVATION_DAYS = 0

# HTTPS
if not DEBUG:
    USE_HTTPS = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_DOMAIN = '.snipt.net'

# Messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# User absolute URLs
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/%s/" % u.username,
}

# Caching

# Search
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr'
    },
}

# Extensions
if DEBUG:
    INSTALLED_APPS += ('django_extensions',)
