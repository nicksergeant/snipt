# Copy this file to local_settings.py and change it as needed.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

EMAIL_BACKEND = 'postmark.backends.PostmarkBackend'
POSTMARK_API_KEY = ''

SECRET_KEY = ''

DATABASES = {
    'default': {
        'ENGINE': 'sqlite3',
        'NAME': '/path/to/db/',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

VIRTUALENV_PATH = '/path/to/virtualenv/'
