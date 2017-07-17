"""Giza URL Configuration"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.show_giza,
        name="show giza"
    ),
    url(
        r'^all/$',
        views.show_all_giza,
        name="show all giza"
    ),
    url(
        r'^new/$',
        views.new_giza,
        name='new giza'
    ),
    url(
        r'^new/(?P<email>.*)/$',
        views.new_giza,
        name='new giza with email'
    ),
    url(
        r'^(?P<id>\d+)/edit/$',
        views.edit_giza,
        name='edit giza'
    ),
    url(
        r'^(?P<id>\d+)/delete/$',
        views.delete_giza,
        name='delete giza'
    ),
    url(
        r'^search/(?P<search_type>.*)/(?P<search_word>.*)/$',
        views.search_giza,
        name='search giza'
    )
]
