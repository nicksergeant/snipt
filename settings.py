# Django settings for snipt project.

import os

INTERNAL_IPS = ('127.0.0.1',)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
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
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'blogs.middleware.BlogMiddleware',
    'bugsnag.django.middleware.BugsnagMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'snipt.urls'

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates')
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
        #'django.request': {
            #'handlers': ['mail_admins'],
            #'level': 'ERROR',
            #'propagate': True,
        #},
    }
}

# Account settings
LOGIN_REDIRECT_URL = '/'
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

# Bugsnag
BUGSNAG = {
    "api_key": "",
    "project_root": PROJECT_PATH,
}

try:
    from local_settings import *
except ImportError:
    pass
