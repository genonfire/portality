#-*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ValidationError

def validate_image(attached):
    size = attached.file.size
    if size > settings.GIZA_IMAGE_SIZE_LIMIT:
        raise ValidationError("사진 파일은 100KB 이하로 올려주세요.")

class Giza(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)
    name = models.CharField(max_length="30")
    email = models.CharField(max_length="50")
    twitter = models.CharField(max_length="50", blank=True)
    facebook = models.CharField(max_length="50", blank=True)
    belongto = models.CharField(max_length="20", choices=settings.MEDIA_CHOICE, default='한겨레')
    portrait = models.ImageField(upload_to="portrait/", blank=True, validators=[validate_image])
    profile = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse_lazy('show all giza')
