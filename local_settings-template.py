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

SECRET_KEY = ''

DEFAULT_FROM_EMAIL = 'support@snipt.net'
SERVER_EMAIL = 'support@snipt.net'
EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'
POSTMARK_API_KEY = ''

VIRTUALENV_PATH = ''

AMAZON_API_KEY = ''
AMAZON_API_SECRET = ''

STRIPE_API_KEY = ''

ENV_HOST = 'user@domain.com:22'
