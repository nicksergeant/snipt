# Django settings for snipt project.

import os

DEBUG = True

BASE_PATH = os.path.dirname(__file__)

ADMINS = (
    ('Name', 'name@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'snipt'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASS', ''),
        'HOST': os.environ.get('DB_PORT_5432_TCP_ADDR', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT_5432_TCP_PORT', ''),
    }
}

INTERNAL_IPS = ('127.0.0.1',)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Local time zone. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
#
# On Unix systems, a value of None will cause Django to use the same timezone as
# the operating system. On a Windows environment, this must be set to the same
# as your system time zone
TIME_ZONE = 'America/New_York'
USE_TZ = True

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

SECRET_KEY = 'changethis'

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
    'jobs',
    'snipts',
    'utils',
)

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
    'django.contrib.messages.context_processors.messages',
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

AUTHENTICATION_BACKENDS = (
    'utils.backends.EmailOrUsernameModelBackend',
)

ROOT_URLCONF = 'urls'

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates')
)

SESSION_COOKIE_AGE = 15801100

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        #'mail_admins': {
            #'level': 'ERROR',
            #'filters': ['require_debug_false'],
            #'class': 'django.utils.log.AdminEmailHandler'
        #}
    },
    'loggers': {
        #'django.request': {
            #'handlers': ['mail_admins'],
            #'level': 'ERROR',
            #'propagate': True,
        #},
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# Account settings
LOGIN_REDIRECT_URL = '/login-redirect/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
ACCOUNT_ACTIVATION_DAYS = 0

# Messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

# User absolute URLs
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/%s/" % u.username,
}

# Accounts
AUTH_PROFILE_MODULE = 'accounts.UserProfile'

# API
TASTYPIE_CANNED_ERROR = "There was an error with your request. The site developers have a record of this error, please email api@snipt.net and we'll help you out."

try:
    from settings_local import *
except ImportError:
    pass
