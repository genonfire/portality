#-*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse_lazy

class Giza(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)
    name = models.CharField(max_length="30")
    email = models.CharField(max_length="50")
    twitter = models.CharField(max_length="50", blank=True)
    facebook = models.CharField(max_length="50", blank=True)
    belongto = models.CharField(max_length="20", blank=True)
    portrait = models.ImageField(upload_to="portrait/", blank=True)
    profile = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse_lazy('show giza')
