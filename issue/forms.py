# -*- coding: utf-8 -*-
from django import forms
from issue.models import Issue


class IssueEditForm(forms.ModelForm):
    """Issue edit form"""

    class Meta:
        """Meta for IssueEditForm"""

        model = Issue
        exclude = ('datetime', 'count', 'goodcount', 'claimusers',)
