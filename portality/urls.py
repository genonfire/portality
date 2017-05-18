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
    url(r'^$', 'issue.views.show_issues', name="show issues"),
    url(r'^issue/new/$', 'issue.views.new_issue', name="new issue"),
    url(r'^issue/(?P<id>\d+)/edit/$', 'issue.views.edit_issue', name="edit issue"),
    url(r'^db/all/$', 'giza.views.show_all_giza', name="show all giza"),
    url(r'^db/$', 'giza.views.show_giza', name="show giza"),
    url(r'^db/new/$', 'giza.views.new_giza', name="new giza"),
    url(r'^db/(?P<id>\d+)/edit/$', 'giza.views.edit_giza', name="edit giza"),
    url(r'^db/search/(?P<searchType>.*)/(?P<searchWord>.*)/$', 'giza.views.search_giza', name="search giza"),
    url(r'^api/call/$', views.api_issue),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
