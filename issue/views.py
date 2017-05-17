from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import datetime

from models import Issue
from giza.models import Giza
from issue.forms import IssueEditForm
from issue.serializers import IssueSerializer

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
                # existArticle = get_object_or_404(Issue, pk = articleCheck.id)
                updateForm = IssueEditForm(request.POST, request.FILES, instance=articleCheck)
                if updateForm.is_valid():
                    updateArticle = updateForm.save(commit=False)
                    updateArticle.count = updateArticle.count + 1
                    updateArticle.save()

                    return redirect(articleCheck.get_absolute_url())
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

@csrf_exempt
def api_issue(request):
    if request.method == 'GET':
        issues = Issue.objects.all()
        serializer = IssueSerializer(issues, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        articleCheck = Issue.objects.filter(url=request.POST['url'])
        print articleCheck.count()
        if articleCheck.count() == 1:
            serializer = IssueSerializer(data=request.POST)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
        elif articleCheck.count() == 0:
            serializer = IssueSerializer(data=request.POST)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

