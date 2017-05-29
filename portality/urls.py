"""portality URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from issue import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
#    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/login/', 'django.contrib.auth.views.login', name='login', kwargs={'template_name': 'login.html'}),
    url(r'^accounts/logout/', 'django.contrib.auth.views.logout', name='logout', kwargs={'next_page': 'login'}),
    url(r'^accounts/passwordchange/', 'django.contrib.auth.views.password_change', {'post_change_redirect': 'login'}, name='passwordchange'),
    url(r'^accounts/signup/', 'giza.views.sign_up', name='signup'),
    url(r'^accounts/checkduplication/', 'giza.views.check_duplication', name='check duplication'),
    url(r'^accounts/checkvalidation/', 'giza.views.check_validation', name='check validation'),
    url(r'^accounts/checkemail/', 'giza.views.check_email', name='check email'),
    url(r'^accounts/sendemail/', 'giza.views.send_email', name='send email'),
    url(r'^$', 'issue.views.show_issues', name="show issues"),
    url(r'^(?P<nolook>\w+)$', 'issue.views.show_issues', name="show good issues"),
    url(r'^issue/all/(?P<nolook>\w+)$', 'issue.views.show_all_issues', name="show all issues"),
    url(r'^issue/recent/(?P<nolook>\w+)$', 'issue.views.show_recent_issues', name="show recent issues"),
    url(r'^ranking/$', 'issue.views.ranking', name="ranking"),
    url(r'^ranking/(?P<nolook>\w+)$', 'issue.views.ranking', name="ranqueen"),
    url(r'^issue/new/(?P<nolook>\w+)$', 'issue.views.new_issue', name="new issue"),
    url(r'^issue/(?P<id>\d+)/edit/$', 'issue.views.edit_issue', name="edit issue"),
    url(r'^issue/(?P<id>\d+)/delete/$', 'issue.views.delete_issue', name="delete issue"),
    url(r'^issue/search/(?P<searchType>.*)/(?P<searchWord>.*)/$', 'issue.views.search_issue', name="search issue"),
    url(r'^issue/search/(?P<searchType>.*)/(?P<searchWord>.*)/(?P<nolook>\w+)$', 'issue.views.search_issue', name="search good issue"),
    url(r'^issue/(?P<id>\d+)/thumb_down/$', 'issue.views.thumb_down', name="thumb down"),
    url(r'^issue/(?P<id>\d+)/thumb_up/$', 'issue.views.thumb_up', name="thumb up"),
    url(r'^db/all/$', 'giza.views.show_all_giza', name="show all giza"),
    url(r'^db/$', 'giza.views.show_giza', name="show giza"),
    url(r'^db/new/$', 'giza.views.new_giza', name="new giza"),
    url(r'^db/(?P<id>\d+)/edit/$', 'giza.views.edit_giza', name="edit giza"),
    url(r'^db/(?P<id>\d+)/delete/$', 'giza.views.delete_giza', name="delete giza"),
    url(r'^db/search/(?P<searchType>.*)/(?P<searchWord>.*)/$', 'giza.views.search_giza', name="search giza"),
    url(r'^api/call/$', views.api_issue),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
