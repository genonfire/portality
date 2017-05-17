#-*- coding: utf-8 -*-
from giza.models import Giza
from django import forms

class GizaEditForm(forms.ModelForm):
    class Meta:
        model = Giza
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(GizaEditForm, self).__init__(*args, **kwargs)
