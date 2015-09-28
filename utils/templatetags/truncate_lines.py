from django import template

register = template.Library()


@register.filter
def truncate_lines(text):
    return '\n'.join(text.split('\n')[:300])
