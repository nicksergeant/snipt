from django import template
from settings_local import INTERCOM_SECRET_KEY

import hmac, hashlib

register = template.Library()

@register.filter
def intercom_sha_256(user_id):
    return hmac.new(INTERCOM_SECRET_KEY, str(user_id), digestmod=hashlib.sha256).hexdigest()
