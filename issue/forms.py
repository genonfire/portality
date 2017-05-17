#-*- coding: utf-8 -*-
from issue.models import Issue
from django import forms

class IssueEditForm(forms.ModelForm):
    class Meta:
        model = Issue
        exclude = ('datetime', 'count',)
