from django import template

register = template.Library()


@register.filter
def user_is_member(team, user):
    return team.user_is_member(user)
