from django import template

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Variable, Constant
from pygments.lexers import get_all_lexers

from snipts.models import Favorite, Snipt

import hashlib


register = template.Library()

@tag(register, [Constant('as'), Variable()])
def snipt_is_favorited_by_user(context, asvar):

    user = context['request'].user
    snipt = context['snipt']

    is_favorited = False

    if user.is_authenticated():
        if snipt.user != user:
            try:
                is_favorited = Favorite.objects.get(snipt=snipt, user=user).id
            except Favorite.DoesNotExist:
                pass

    context[asvar] = is_favorited

    return ''

@tag(register, [])
def snipts_count_for_user(context):

    user = context['request'].user

    if user.is_authenticated():
        snipts = Snipt.objects.filter(user=user).values('id').count()
    else:
        snipts = 0

    return snipts

@tag(register, [Constant('as'), Variable()])
def get_lexers(context, asvar):

    context[asvar] = sorted(get_all_lexers())

    return ''


@register.filter
def md5(string):
    return hashlib.md5(string.lower()).hexdigest()
