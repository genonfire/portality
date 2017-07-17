from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name='is_inweek')
def _is_inweek(created_at):
    if created_at > timezone.now() - timezone.timedelta(days=7):
        return True
    else:
        return False
