import hmac
import hashlib
import os

from django import template
from django.conf import settings

register = template.Library()


@register.filter
def intercom_sha_256(user_id):
    return hmac.new(os.environ.get('INTERCOM_SECRET_KEY',
                                   settings.INTERCOM_SECRET_KEY),
                    str(user_id),
                    digestmod=hashlib.sha256).hexdigest()
