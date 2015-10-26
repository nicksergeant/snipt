import datetime

from django import template

register = template.Library()


@register.filter
def user_is_member(team, user):
    return team.user_is_member(user)


@register.filter
def currency_convert(amount):
    return amount / 100


@register.filter
def to_date(timestamp):
    return datetime.datetime.fromtimestamp(float(timestamp))
