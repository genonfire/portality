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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(
        r'^accounts/login/$',
        'django.contrib.auth.views.login',
        name='login',
        kwargs={'template_name': 'login.html'}
    ),
    url(
        r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        name='logout',
        kwargs={'next_page': 'login'}
    ),
    url(
        r'^accounts/passwordchange/$',
        'django.contrib.auth.views.password_change',
        name='passwordchange'
    ),
    url(
        r'^accounts/passwordreset/$',
        'django.contrib.auth.views.password_reset',
        name='passwordreset'
    ),
    url(r'^$', 'issue.views.show_news', name="show news"),
    url(r'^(?P<page>\d+)$', 'issue.views.show_news', name="show news+"),
    url(r'^best/$', 'issue.views.show_issues', name="show issues"),
    url(r'^best/(?P<nolook>\w+)$', 'issue.views.show_issues', name="show issues+"),
    url(r'^best/(?P<page>\d+)/(?P<nolook>\w+)$', 'issue.views.show_best_issues', name="show best issues"),
    url(r'^ranking/$', 'issue.views.ranking', name="ranking default"),
    url(r'^ranking/(?P<nolook>\w+)$', 'issue.views.ranking', name="ranking"),
    url(r'^ranking/(?P<ranktype>\w+)/(?P<nolook>\w+)$', 'issue.views.ranking', name="rank all"),
    url(r'^ranking/(?P<year>\d+)/(?P<month>\d+)/(?P<nolook>\w+)$', 'issue.views.rank_archive', name="rank archive"),
    url(r'^ranking/(?P<year>\d+)/(?P<month>\d+)/(?P<nolook>\w+)/(?P<day>\d+)$', 'issue.views.rank_archive', name="rank specify"),
    url(r'^issue/new/(?P<nolook>\w+)$', 'issue.views.new_issue', name="new issue"),
    url(r'^issue/(?P<id>\d+)/edit/$', 'issue.views.edit_issue', name="edit issue"),
    url(r'^issue/(?P<id>\d+)/delete/$', 'issue.views.delete_issue', name="delete issue"),
    url(r'^issue/search/(?P<search_range>\w+)/(?P<search_type>.*)/(?P<search_word>.*)/(?P<nolook>\w+)$', 'issue.views.search_issue', name="search issue"),
    url(r'^issue/search/(?P<search_range>\w+)/(?P<search_type>\w+)/(?P<search_word>.*)/(?P<nolook>\w+)/(?P<page>\d+)/$', 'issue.views.search_issue', name="search issue+"),
    url(r'^chart/(?P<year>\d+)/(?P<month>\d+)/$', 'issue.views.chart_archive', name="chart archive", kwargs={'chartfrom': 'archive'}),
    url(r'^chart/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'issue.views.chart_archive', name="chart specify", kwargs={'chartfrom': 'specify'}),
    url(r'^chart/$', 'issue.views.chart', name="chart"),
    url(r'^podcast/(?P<pod>\w+)/$', 'core.views.podcast', name="podcast"),
    url(r'^db/', include('giza.urls', namespace='giza')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^api/', include('core.apiurls', namespace='api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
