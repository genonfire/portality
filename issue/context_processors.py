from django.conf import settings

def global_settings(request):
    return {
        'DEBUG': settings.DEBUG,
        'ABOUT_LINK': settings.ABOUT_LINK,
        'LOGO_NAME': settings.LOGO_NAME,
        'THEME_DESIGNER': settings.THEME_DESIGNER,
    }
