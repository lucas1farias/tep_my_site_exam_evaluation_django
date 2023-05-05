

from django import template
register = template.Library()


@register.filter(name='get_type')
def get_type(value):
    return type(value).__name__


@register.filter(name='turn_into_string')
def turn_into_string(content):
    return str(content)
