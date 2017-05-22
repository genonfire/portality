from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.db.models import Sum
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
    startdate = timezone.now() - timezone.timedelta(days=settings.FILTER_DATE_DELTA)
    enddate = timezone.now()
    issues = Issue.objects.filter(datetime__range=(startdate, enddate)).order_by('-count')[0:settings.HOTISSUE_LIMIT]

    return render(
        request,
        "hotissue.html",
        {
            'issues' : issues,
        }
    )

def search_issue(request, searchType, searchWord):
    issues = None
    if searchType == "subject":
        issues = Issue.objects.filter(subject__icontains=searchWord).order_by('-count', '-datetime')
    elif searchType == "url":
        issues = Issue.objects.filter(url__iexact=searchWord).order_by('-count', '-datetime')
    elif searchType == "email":
        issues = Issue.objects.filter(email__icontains=searchWord).order_by('-count', '-datetime')
    elif searchType == "name":
        giza = Giza.objects.filter(name__iexact=searchWord)
        if giza.exists():
            emails = giza.values_list('email', flat=True)
            issues = Issue.objects.filter(email__in=emails)
    elif searchType == "belongto":
        giza = Giza.objects.filter(belongto__icontains=searchWord)
        if giza.exists():
            emails = giza.values_list('email', flat=True)
            issues = Issue.objects.filter(email__in=emails)

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
            'created_at': issue.datetime,
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

def getKey(item):
    return item[1]

def ranking(request):
    startdate = timezone.now() - timezone.timedelta(days=settings.RANKING_DATE_DELTA)
    enddate = timezone.now()
    issues = Issue.objects.exclude(email__iexact='').filter(datetime__range=(startdate, enddate)).order_by('email', '-count').select_related('email', 'count')
    emails = issues.distinct('email').values_list('email', flat=True)

    countList = []

    for email in emails:
        count = issues.filter(email__iexact=email).aggregate(total_count=Sum('count'))
        giza = Giza.objects.filter(email__iexact=email)
        if giza.exists():
            countList.append((giza[0], count['total_count']))

    listRank = sorted(countList, key=getKey, reverse=True)

    return render(
        request,
        "ranking.html",
        {
            'lists': listRank,
        }
    )
