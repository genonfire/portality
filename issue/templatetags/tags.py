from django import template
register = template.Library()

@register.simple_tag
def getIndex(counter, index):
    new_index = (int(index) - 1) * 10 + counter
    return new_index
