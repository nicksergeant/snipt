from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
