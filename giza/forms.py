#-*- coding: utf-8 -*-
from giza.models import Giza
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class GizaEditForm(forms.ModelForm):
    class Meta:
        model = Giza
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(GizaEditForm, self).__init__(*args, **kwargs)

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='email', required=True)
    code = forms.CharField(label='code', required=False)

    class Meta:
        model = User
        fields = {"username", "email", "code"}

    # def __init__(self, *args, **kwargs):
    #     super(UserCreationForm, self).__init__(*args, **kwargs)
