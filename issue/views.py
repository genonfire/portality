from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import datetime

from models import Issue
from giza.models import Giza
from issue.forms import IssueEditForm

from django.conf import settings

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def show_issues(request):
    startdate = datetime.date.today()
    enddate = startdate + datetime.timedelta(days=settings.FILTER_DATE_DELTA)
    issues = Issue.objects.filter(datetime__range=(startdate, enddate)).order_by('-count')[0:settings.HOTISSUE_LIMIT]

    return render(
        request,
        "hotissue.html",
        {
            'issues' : issues,
        }
    )

def new_issue(request):
    if request.method == "POST":
        editform = IssueEditForm(request.POST, request.FILES)
        if editform.is_valid():
            article = editform.save(commit=False)
            try:
                articleCheck = Issue.objects.filter(url=article.url).get()
                existArticle = get_object_or_404(Issue, pk = articleCheck.id)
                updateForm = IssueEditForm(request.POST, request.FILES, instance=existArticle)
                if updateForm.is_valid():
                    updateArticle = updateForm.save(commit=False)
                    updateArticle.count = updateArticle.count + 1
                    updateArticle.save()

                    return redirect(existArticle.get_absolute_url())
            except ObjectDoesNotExist:
                article.count = 1
                article.save()

                return redirect(article.get_absolute_url())
    elif request.method == "GET":
        editform = IssueEditForm()

    return render(
        request,
        'editissue.html',
        {
            'form': editform,
        }
    )

@login_required
def edit_issue(request, id):
    issue = get_object_or_404(Issue, pk = id)

    if request.method == "POST":
        editform = IssueEditForm(request.POST, request.FILES, instance=issue)
        if editform.is_valid():
            editform.save()
            return redirect(issue.get_absolute_url())
    elif request.method == "GET":
        editform = IssueEditForm(instance=issue)

    return render(
        request,
        'editissue.html',
        {
            'form': editform,
        }
    )
