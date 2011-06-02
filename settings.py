import os.path

BASE_PATH = os.path.dirname(__file__)

ADMINS = (
    ('Nick Sergeant', 'nick@snipt.net'),
)
MANAGERS = ADMINS

INTERNAL_IPS = ('127.0.0.1',)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = os.path.join(BASE_PATH, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = 'm5w4e9^9r69f!6b9qio%)_p%a*1d(waqki+r_g11=qijh=#wuk'

SESSION_COOKIE_AGE = 31556926

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'grappelli.context_processors.admin_template_path',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = os.path.join(BASE_PATH, 'templates')

INSTALLED_APPS = (
    'grappelli',
    'admin_tools.theming',
    'admin_tools.menu',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.redirects',

    'compressor',
    'django_bcrypt',
    'south',
)

# CSS compression

COMPRESS_OUTPUT_DIR = "cache"
COMPILER_FORMATS = {
    '.less': {
        'binary_path':'lessc',
        'arguments': '*.less *.css'
    },
}

# Grappelli

GRAPPELLI_ADMIN_TITLE = '<a href="/">Snipt</a>'

# Local settings and debug

from local_settings import *

if DEBUG:
    INSTALLED_APPS += ('django_extensions',)
