from django import template

register = template.Library()


@register.filter
def mod(num, val):
    return num % val


@register.filter
def trim_trailing_zeroes(num):
    return ('%f' % num).rstrip('0').rstrip('.') if isinstance(num, float) else None
