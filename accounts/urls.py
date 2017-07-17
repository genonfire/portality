"""accounts URL Configuration"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^signup/$',
        views.sign_up,
        name='signup'
    ),
    url(
        r'^checkduplication/$',
        views.check_duplication,
        name='check_duplication'
    ),
    url(
        r'^checkvalidation/$',
        views.check_validation,
        name='check_validation'
    ),
    url(
        r'^checkemail/$',
        views.check_email,
        name='check_email',
    ),
    url(
        r'^sendemail/$',
        views.send_email,
        name='send_email'
    ),
    url(
        r'^updateallusers/$',
        views.update_all_users,
        name='update_all_users'
    ),
    url(
        r'^showallusers/$',
        views.show_all_users,
        name='show_all_users'
    ),
]
