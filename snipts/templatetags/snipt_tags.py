from django import template

from snipts.models import Favorite

register = template.Library()


@register.filter
def is_favorited_by(snipt, user):
    try:
        Favorite.objects.get(snipt=snipt, user=user)
        return True
    except Favorite.DoesNotExist:
        return False
