import dj_database_url, os

ABSOLUTE_URL_OVERRIDES = { 'auth.user': lambda u: "/%s/" % u.username, }
ACCOUNT_ACTIVATION_DAYS = 0
ADMINS = (('Name', 'name@domain.com'),)
ALLOWED_HOSTS = ['*']
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
AUTHENTICATION_BACKENDS = ('utils.backends.EmailOrUsernameModelBackend',)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.dirname(__file__)
DATABASES = { 'default': dj_database_url.config() }
DEBUG = True
HAYSTACK_CONNECTIONS = { 'default': { 'ENGINE': 'haystack.backends.simple_backend.SimpleEngine', }, }
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
INTERNAL_IPS = ('127.0.0.1',)
LANGUAGE_CODE = 'en-us'
LOGIN_REDIRECT_URL = '/login-redirect/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
MANAGERS = ADMINS
MEDIA_ROOT = os.path.join(BASE_PATH, 'media/uploads')
MEDIA_URL = '/media/uploads/'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_URLCONF = 'urls'
SECRET_KEY = 'changethis'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_AGE = 15801100
SITE_ID = 1
STATICFILES_DIRS = (os.path.join(BASE_PATH, 'media'),)
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder','django.contrib.staticfiles.finders.AppDirectoriesFinder',)
STATIC_ROOT = os.path.join(BASE_PATH, 'static')
STATIC_URL = '/static/'
TASTYPIE_CANNED_ERROR = "There was an error with your request. The site developers have a record of this error, please email api@snipt.net and we'll help you out."
TEMPLATE_DIRS = (os.path.join(PROJECT_PATH, 'templates'))
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

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
