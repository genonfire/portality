"""API URL Configuration"""

from django.conf.urls import url

from . import api

urlpatterns = [
    url(
        r'^call/$',
        api.api_issue,
        name='api_issue'
    ),
    url(
        r'^thumb_down/$',
        api.api_vote,
        name='api_thumb_down',
        kwargs={'liketype': 'dislike'}
    ),
    url(
        r'^thumb_up/$',
        api.api_vote,
        name='api_thumb_up',
        kwargs={'liketype': 'like'}
    ),
    url(
        r'^burst_call/$',
        api.api_burst_call,
        name='api_burst_call'
    ),
]
