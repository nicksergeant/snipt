import dj_database_url
import os

from urlparse import urlparse


if 'DATABASE_URL' in os.environ:

    DATABASES = {'default': dj_database_url.config()}

    es = urlparse(os.environ.get('SEARCHBOX_SSL_URL') or
                  'http://127.0.0.1:9200/')
    port = es.port or 80

    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'URL': es.scheme + '://' + es.hostname + ':' + str(port),
            'INDEX_NAME': 'snipts',
        },
    }

    if es.username:
        HAYSTACK_CONNECTIONS['default']['KWARGS'] = {
            "http_auth": es.username + ':' + es.password
        }

ABSOLUTE_URL_OVERRIDES = {'auth.user': lambda u: "/%s/" % u.username}
ACCOUNT_ACTIVATION_DAYS = 0
ADMINS = (('Nick Sergeant', 'nick@snipt.net'),)
ALLOWED_HOSTS = ['*']
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
AUTHENTICATION_BACKENDS = ('utils.backends.EmailOrUsernameModelBackend',)
BASE_PATH = os.path.dirname(__file__)
CSRF_COOKIE_DOMAIN = '.snipt.net' if 'USE_SSL' in os.environ else False
CSRF_COOKIE_SECURE = True if 'USE_SSL' in os.environ else False
DEBUG = True if 'DEBUG' in os.environ else False
DEFAULT_FROM_EMAIL = 'support@snipt.net'
EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
INTERCOM_SECRET_KEY = os.environ.get('INTERCOM_SECRET_KEY', '')
INTERNAL_IPS = ('127.0.0.1',)
LANGUAGE_CODE = 'en-us'
LOGIN_REDIRECT_URL = '/login-redirect/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
MANAGERS = ADMINS
MEDIA_ROOT = os.path.join(BASE_PATH, 'media/uploads')
MEDIA_URL = '/media/uploads/'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)
POSTMARK_API_KEY = os.environ.get('POSTMARK_API_KEY', '')
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
RAVEN_CONFIG = {'dsn': os.environ.get('RAVEN_CONFIG_DSN', '')}
REGISTRATION_EMAIL_HTML = False
ROOT_URLCONF = 'urls'
SECRET_KEY = os.environ.get('SECRET_KEY', 'changeme')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SEND_BROKEN_LINK_EMAILS = False
SERVER_EMAIL = 'support@snipt.net'
SESSION_COOKIE_AGE = 15801100
SESSION_COOKIE_SECURE = True if 'USE_SSL' in os.environ else False
SITE_ID = 1
STATICFILES_DIRS = (os.path.join(BASE_PATH, 'media'),)
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder',
                       'django.contrib.staticfiles.finders.AppDirectoriesFinder')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_PATH, 'static')
STATIC_URL = '/static/'
TASTYPIE_CANNED_ERROR = """There was an error with your request. The site
    developers have a record of this error, please email api@snipt.net and
    we'll help you out."""
TEMPLATE_DIRS = (os.path.join(PROJECT_PATH, 'templates'),)
TEMPLATE_DEBUG = DEBUG
TIME_ZONE = 'America/New_York'
USE_HTTPS = True if 'USE_SSL' in os.environ else False
USE_I18N = True
USE_L10N = True
USE_TZ = True

INSTALLED_APPS = (
    'accounts',
    'blogs',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_extensions',
    'gunicorn',
    'haystack',
    'markdown_deux',
    'pagination',
    'postmark',
    'raven.contrib.django.raven_compat',
    'registration',
    'snipts',
    'storages',
    'taggit',
    'tastypie',
    'teams',
    'typogrify',
    'user-admin',
    'utils',
)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {},
    'loggers': {}
}
MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'blogs.middleware.BlogMiddleware',
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
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

try:
    from settings_local import *
except ImportError:
    pass
