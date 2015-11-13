import hashlib

from django import template
from snipts.models import Favorite, Snipt
from snipts.utils import get_lexers_list
from templatetag_sugar.parser import Variable, Constant
from templatetag_sugar.register import tag

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
    context[asvar] = get_lexers_list()
    return ''


@tag(register, [Constant('for'), Variable()])
def generate_line_numbers(context, line_numbers):
    html = ''

    for i in range(1, line_numbers + 1):
        html = html + '<span class="special">{}</span>'.format(i)

    return html


@register.filter
def md5(string):
    return hashlib.md5(string.lower().encode('utf-8')).hexdigest()


@register.filter
def is_authorized_user(snipt, user):
    return snipt.is_authorized_user(user)
