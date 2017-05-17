from django.conf import settings

def global_settings(request):
    return {
        'FILTER_DATE_DELTA': settings.FILTER_DATE_DELTA,
        'HOTISSUE_LIMIT': settings.HOTISSUE_LIMIT,
    }
