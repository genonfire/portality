from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def getIndex(counter, index):
    acom = settings.BEST_LIST_LIMIT / 10
    new_index = (int(index) * acom - acom) * 10 + counter
    return new_index
