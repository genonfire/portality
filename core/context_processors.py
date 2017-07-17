from django.conf import settings


def global_settings(request):
    """Setting for templates"""
    return {
        'DEBUG': settings.DEBUG,
        'BURST_CALL_ACOM': settings.BURST_CALL_ACOM,
        'ABOUT_LINK': settings.ABOUT_LINK,
        'LOGO_NAME': settings.LOGO_NAME,
        'THEME': settings.THEME,
        'NEWBC_LINK': settings.NEWBC_LINK,
        'NEWBC_IMG': settings.NEWBC_IMG,
        'NEWBC_IMG_SMALL': settings.NEWBC_IMG_SMALL,
        'FOOTER_TAGS': settings.FOOTER_TAGS,
    }
