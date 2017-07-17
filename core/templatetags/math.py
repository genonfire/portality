from django import template

register = template.Library()


@register.filter(name='divide')
def _divide(point, acom):
    return float(point) / acom
