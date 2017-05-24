#-*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

from rest_framework import serializers

class Issue(models.Model):
    email = models.CharField(max_length="50", blank=True)
    subject = models.CharField(max_length="100")
    url = models.CharField(max_length="255")
    archive = models.CharField(max_length="255", blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)
    claimusers = models.TextField(default='', blank=True)

    def get_absolute_url(self):
        return reverse_lazy('show issues')
