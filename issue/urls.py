"""issue URL Configuration"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.show_news,
        name='show news'
    ),
    url(
        r'^(?P<page>\d+)$',
        views.show_news,
        name='show news+'
    ),
    url(
        r'^best/$',
        views.show_issues,
        name='show issues'
    ),
    url(
        r'^best/(?P<nolook>\w+)$',
        views.show_issues,
        name='show issues+'
    ),
    url(
        r'^best/(?P<page>\d+)/(?P<nolook>\w+)$',
        views.show_best_issues,
        name='show best issues'
    ),
    url(
        r'^ranking/$',
        views.ranking,
        name='ranking default'
    ),
    url(
        r'^ranking/(?P<nolook>\w+)$',
        views.ranking,
        name='ranking'
    ),
    url(
        r'^ranking/(?P<ranktype>\w+)/(?P<nolook>\w+)$',
        views.ranking,
        name='rank all'
    ),
    url(
        r'^ranking/(?P<year>\d+)/(?P<month>\d+)/(?P<nolook>\w+)$',
        views.rank_archive,
        name='rank archive'
    ),
    url(
        r'^ranking/(?P<year>\d+)/(?P<month>\d+)/(?P<nolook>\w+)/(?P<day>\d+)$',
        views.rank_archive,
        name='rank specify'
    ),
    url(
        r'^issue/new/(?P<nolook>\w+)$',
        views.new_issue,
        name='new issue'
    ),
    url(
        r'^issue/(?P<id>\d+)/edit/$',
        views.edit_issue,
        name='edit issue'
    ),
    url(
        r'^issue/(?P<id>\d+)/delete/$',
        views.delete_issue,
        name='delete issue'
    ),
    url(
        r'^issue/search/(?P<search_range>\w+)/(?P<search_type>.*)/(?P<search_word>.*)/(?P<nolook>\w+)$',
        views.search_issue,
        name='search issue'
    ),
    url(
        r'^issue/search/(?P<search_range>\w+)/(?P<search_type>\w+)/(?P<search_word>.*)/(?P<nolook>\w+)/(?P<page>\d+)/$',
        views.search_issue,
        name='search issue+'
    ),
    url(
        r'^chart/(?P<year>\d+)/(?P<month>\d+)/$',
        views.chart_archive,
        name='chart archive',
        kwargs={'chartfrom': 'archive'}),
    url(
        r'^chart/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
        views.chart_archive,
        name='chart specify',
        kwargs={'chartfrom': 'specify'}),
    url(
        r'^chart/$',
        views.chart,
        name='chart'
    ),
]
