from urllib.parse import urlparse

import dj_database_url
import os

if "DATABASE_URL" in os.environ:
    DATABASES = {"default": dj_database_url.config()}

ABSOLUTE_URL_OVERRIDES = {"auth.user": lambda u: "/%s/" % u.username}
ACCOUNT_ACTIVATION_DAYS = 0
ADMINS = (("Siftie", "team@siftie.com"),)
ALLOWED_HOSTS = ["*"]
AUTH_PROFILE_MODULE = "accounts.UserProfile"
AUTHENTICATION_BACKENDS = ("utils.backends.EmailOrUsernameModelBackend",)
BASE_PATH = os.path.dirname(__file__)
CSRF_COOKIE_SECURE = True if "USE_SSL" in os.environ else False
CORS_ORIGIN_ALLOW_ALL = True
DEBUG = True if "DEBUG" in os.environ else False
DEFAULT_FROM_EMAIL = os.environ.get("POSTMARK_EMAIL", "team@siftie.com")
EMAIL_BACKEND = "postmark.django_backend.EmailBackend"
# HAYSTACK_CONNECTIONS = {
#     "default": {
#         "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
#         "PATH": os.environ.get("WHOOSH_PATH", "./.whoosh_index"),
#         "STORAGE": "file",
#     }
# }
# HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.RealtimeSignalProcessor"
INTERNAL_IPS = ("127.0.0.1",)
LANGUAGE_CODE = "en-us"
LOGIN_REDIRECT_URL = "/login-redirect/"
LOGIN_URL = "/login/"
LOGOUT_URL = "/logout/"
MANAGERS = ADMINS
MEDIA_ROOT = os.path.join(BASE_PATH, "media/uploads")
MEDIA_URL = "/media/uploads/"
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"
PASSWORD_HASHERS = (
    "django.contrib.auth.hashers.BCryptPasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.SHA1PasswordHasher",
    "django.contrib.auth.hashers.MD5PasswordHasher",
    "django.contrib.auth.hashers.CryptPasswordHasher",
)
POSTMARK_API_KEY = os.environ.get("POSTMARK_API_KEY", "")
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
REGISTRATION_EMAIL_HTML = False
ROOT_URLCONF = "urls"
SECRET_KEY = os.environ.get("SECRET_KEY", "changeme")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True if "USE_SSL" in os.environ else False
SEND_BROKEN_LINK_EMAILS = False
SERVER_EMAIL = os.environ.get("POSTMARK_EMAIL", "team@siftie.com")
SESSION_COOKIE_AGE = 15801100
SESSION_COOKIE_SECURE = True if "USE_SSL" in os.environ else False
SITE_ID = 1
STATICFILES_DIRS = (os.path.join(BASE_PATH, "media"),)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
STATICFILES_STORAGE = "whitenoise.django.GzipManifestStaticFilesStorage"
STATIC_ROOT = os.path.join(BASE_PATH, "static")
STATIC_URL = "/static/"
TASTYPIE_CANNED_ERROR = """There was an error with your request. The site
    developers have a record of this error, please email team@siftie.com and
    we'll help you out."""

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_PATH, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

TIME_ZONE = "America/New_York"
USE_HTTPS = True if "USE_SSL" in os.environ else False
USE_I18N = True
USE_L10N = True
USE_TZ = True

INSTALLED_APPS = (
    "accounts",
    "blogs",
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django_extensions",
    "gunicorn",
    # "haystack",
    "markdown_deux",
    "pagination",
    "postmark",
    "registration",
    "snipts",
    "storages",
    "taggit",
    "tastypie",
    "teams",
    "user-admin",
    "utils",
)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {},
    "loggers": {},
}
MIDDLEWARE_CLASSES = (
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "pagination.middleware.PaginationMiddleware",
    "blogs.middleware.BlogMiddleware",
)

try:
    from settings_local import *
except ImportError:
    pass
