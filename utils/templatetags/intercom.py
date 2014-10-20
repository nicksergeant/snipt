from django import template

import hmac, hashlib, os

register = template.Library()

@register.filter
def intercom_sha_256(user_id):
    return hmac.new(os.environ.get('INTERCOM_SECRET_KEY', ''), str(user_id), digestmod=hashlib.sha256).hexdigest()
