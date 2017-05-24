from django.conf import settings

def global_settings(request):
    return {
        'ABOUT_LINK': settings.ABOUT_LINK,
    }
