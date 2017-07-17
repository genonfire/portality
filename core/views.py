# -*- coding: utf-8 -*-
import sys

from django.http import HttpResponse

from podcast import newsfactory

reload(sys)
sys.setdefaultencoding('utf-8')


def podcast(request, pod='newsfactory'):
    u"""Podcast"""
    if pod == 'newsfactory':
        response = HttpResponse(newsfactory(), content_type='application/rss+xml')
    return response
