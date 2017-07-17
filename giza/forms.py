# -*- coding: utf-8 -*-
from django import forms

from giza.models import Giza


class GizaEditForm(forms.ModelForm):
    """Giza edit form"""

    class Meta:
        """Meta for GizaEditForm"""

        model = Giza
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """Init"""
        self.user = kwargs.pop('user', None)
        super(GizaEditForm, self).__init__(*args, **kwargs)
