# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.db import models


def validate_image(attached):
    """Validator for image uploading"""
    size = attached.file.size
    if size > settings.GIZA_IMAGE_SIZE_LIMIT:
        raise ValidationError("사진 파일은 100KB 이하로 올려주세요.")


class Giza(models.Model):
    """Class Giza"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True)
    name = models.CharField(max_length="30")
    email = models.CharField(max_length="50")
    twitter = models.CharField(max_length="50", blank=True)
    facebook = models.CharField(max_length="100", blank=True)
    belongto = models.CharField(max_length="20", choices=settings.MEDIA_CHOICE, default='한겨레')
    portrait = models.ImageField(upload_to="portrait/", blank=True, validators=[validate_image])
    profile = models.TextField(blank=True)

    def get_absolute_url(self):
        """Default return URL"""
        return reverse_lazy('giza:show giza')

    def get_serach_url(self, email):
        """Return URL for New giza"""
        return reverse_lazy('giza:search giza', kwargs={'search_type': 'email', 'search_word': email})

    def save(self, *args, **kwargs):
        """To delete attached if changed"""
        try:
            this = Giza.objects.get(id=self.id)
            if this.portrait != self.portrait:
                this.portrait.delete()
        except:
            pass
        super(Giza, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """To delete attached too"""
        self.portrait.delete()
        super(Giza, self).delete(*args, **kwargs)
