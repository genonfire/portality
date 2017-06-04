#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
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
from portality.utils import *

from django.conf import settings

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

@user_passes_test(lambda u: u.is_superuser)
def show_all_issues(request, nolook):
    if nolook == 'nolook':
        issues = Issue.objects.filter(count__gte=1).order_by('-datetime')
    else:
        issues = Issue.objects.filter(goodcount__gte=1).order_by('-datetime')

    template = "hotissue.html"
    if is_mobile(request):
        template = "m-hotissue.html"

    return render(
        request,
        template,
        {
            'issues' : issues,
            'nolook' : nolook,
        }
    )

def show_issues(request, nolook='nolook'):
    threshold = settings.BEST_THRESHOLD
    limit = settings.BEST_LIST_LIMIT
    nextPage = 0

    if nolook == 'nolook':
        total = Issue.objects.filter(count__gte=threshold).count()
    else:
        total = Issue.objects.filter(goodcount__gte=threshold).count()

    cut, reminder = divmod(total, limit)
    if (reminder > 0):
        cut += 1
    if (cut > 1):
        nextPage = 2

    if nolook == 'nolook':
        issues = Issue.objects.filter(count__gte=threshold).order_by('-datetime')[0:limit]
    else:
        issues = Issue.objects.filter(goodcount__gte=threshold).order_by('-datetime')[0:limit]

    template = "hotissue.html"
    if is_mobile(request):
        template = "m-hotissue.html"

    return render(
        request,
        template,
        {
            'issues' : issues,
            'nolook' : nolook,
            'index' : 1,
            'total' : total,
            'prevPage' : 0,
            'nextPage' : nextPage,
            'searchRange' : 'best',
        }
    )

def show_best_issues(request, page, nolook='nolook'):
    threshold = settings.BEST_THRESHOLD
    limit = settings.BEST_LIST_LIMIT
    nextPage = 0
    currentPage = int(page)
    prevPage = currentPage - 1
    startPage = prevPage * limit

    if nolook == 'nolook':
        total = Issue.objects.filter(count__gte=threshold).count()
    else:
        total = Issue.objects.filter(goodcount__gte=threshold).count()

    cut, reminder = divmod(total, limit)
    if (reminder > 0):
        cut += 1
    if (cut > currentPage):
        nextPage = currentPage + 1

    if nolook == 'nolook':
        issues = Issue.objects.filter(count__gte=threshold).order_by('-datetime')[startPage:startPage+limit]
    else:
        issues = Issue.objects.filter(goodcount__gte=threshold).order_by('-datetime')[startPage:startPage+limit]

    template = "hotissue.html"
    if is_mobile(request):
        template = "m-hotissue.html"

    return render(
        request,
        template,
        {
            'issues' : issues,
            'nolook' : nolook,
            'index' : page,
            'total' : total,
            'prevPage' : prevPage,
            'nextPage' : nextPage,
            'searchRange' : 'best',
        }
    )

def show_today_issues(request, nolook='nolook'):
    startdate = timezone.now() - timezone.timedelta(days=settings.HOTISSUE_DATE_DELTA)
    enddate = timezone.now()

    if nolook == 'nolook':
        issues = Issue.objects.filter(count__gte=1).filter(datetime__range=(startdate, enddate)).order_by('-count')[0:settings.HOTISSUE_LIMIT]
    else:
        issues = Issue.objects.filter(goodcount__gte=1).filter(datetime__range=(startdate, enddate)).order_by('-goodcount')[0:settings.HOTISSUE_LIMIT]

    template = "hotissue.html"
    if is_mobile(request):
        template = "m-hotissue.html"

    return render(
        request,
        template,
        {
            'issues' : issues,
            'nolook' : nolook,
            'today' : True,
            'searchRange' : 'all',
        }
    )

def show_today_all(request, nolook='nolook'):
    startdate = timezone.now() - timezone.timedelta(days=settings.HOTISSUE_DATE_DELTA)
    enddate = timezone.now()

    if nolook == 'nolook':
        issues = Issue.objects.filter(count__gte=1).filter(datetime__range=(startdate, enddate)).order_by('-datetime')
    else:
        issues = Issue.objects.filter(goodcount__gte=1).filter(datetime__range=(startdate, enddate)).order_by('-datetime')

    template = "hotissue.html"
    if is_mobile(request):
        template = "m-hotissue.html"

    return render(
        request,
        template,
        {
            'issues' : issues,
            'nolook' : nolook,
            'today' : True,
            'searchRange' : 'all',
        }
    )

def search_issue(request, searchRange, searchType, searchWord, nolook='nolook'):
    issues = nolookissues = lookissues = None
    threshold = 1
    issueCount = 0
    today = True
    if searchRange == 'best':
        threshold = settings.BEST_THRESHOLD
        today = False

    if nolook == 'nolook' or nolook == 'all':
        if searchType == "subject":
            nolookissues = Issue.objects.filter(count__gte=threshold).filter(subject__icontains=searchWord).order_by('-count', '-datetime')
        elif searchType == "url":
            nolookissues = Issue.objects.filter(count__gte=threshold).filter(url__iexact=searchWord).order_by('-count', '-datetime')
        elif searchType == "email":
            nolookissues = Issue.objects.filter(count__gte=threshold).filter(email__icontains=searchWord).order_by('-count', '-datetime')
        elif searchType == "name":
            giza = Giza.objects.filter(name__iexact=searchWord)
            if giza.exists():
                emails = giza.values_list('email', flat=True)
                nolookissues = Issue.objects.filter(count__gte=threshold).filter(email__in=emails)
        elif searchType == "belongto":
            giza = Giza.objects.filter(belongto__icontains=searchWord)
            if giza.exists():
                emails = giza.values_list('email', flat=True)
                nolookissues = Issue.objects.filter(count__gte=threshold).filter(email__in=emails)
        issues = nolookissues
    if nolook == 'look' or nolook == 'all':
        if searchType == "subject":
            lookissues = Issue.objects.filter(goodcount__gte=threshold).filter(subject__icontains=searchWord).order_by('-goodcount', '-datetime')
        elif searchType == "url":
            lookissues = Issue.objects.filter(goodcount__gte=threshold).filter(url__iexact=searchWord).order_by('-goodcount', '-datetime')
        elif searchType == "email":
            lookissues = Issue.objects.filter(goodcount__gte=threshold).filter(email__icontains=searchWord).order_by('-goodcount', '-datetime')
        elif searchType == "name":
            giza = Giza.objects.filter(name__iexact=searchWord)
            if giza.exists():
                emails = giza.values_list('email', flat=True)
                lookissues = Issue.objects.filter(goodcount__gte=threshold).filter(email__in=emails)
        elif searchType == "belongto":
            giza = Giza.objects.filter(belongto__icontains=searchWord)
            if giza.exists():
                emails = giza.values_list('email', flat=True)
                lookissues = Issue.objects.filter(goodcount__gte=threshold).filter(email__in=emails)
        issues = lookissues

    template = "hotissue.html"
    if is_mobile(request):
        template = "m-hotissue.html"

    if issues:
        issueCount = issues.count()

    return render(
        request,
        template,
        {
            'nolookissues' : nolookissues,
            'lookissues' : lookissues,
            'issues' : issues,
            'nolook' : nolook,
            'searchRange' : searchRange,
            'total' : issueCount,
            'today' : today,
        }
    )

def new_issue(request, nolook='nolook'):
    if request.method == "POST":
        editform = IssueEditForm(request.POST, request.FILES)
        if editform.is_valid():
            article = editform.save(commit=False)
            try:
                articleCheck = Issue.objects.filter(url=article.url).get()
                updateForm = IssueEditForm(request.POST, request.FILES, instance=articleCheck)
                if updateForm.is_valid():
                    updateArticle = updateForm.save(commit=False)
                    claimusers = updateArticle.claimusers.split(',')
                    ip = get_ipaddress(request)
                    if ip not in claimusers:
                        updateArticle.claimusers += "," + ip
                        if nolook == 'nolook':
                            updateArticle.count += 1
                        else:
                            updateArticle.goodcount += 1
                    updateArticle.save()
                    return redirect(articleCheck.get_absolute_url(nolook))
            except ObjectDoesNotExist:
                if nolook == 'nolook':
                    article.count = 1
                else:
                    article.goodcount = 1
                article.claimusers = get_ipaddress(request)
                article.save()
                return redirect(article.get_absolute_url(nolook))
    elif request.method == "GET":
        editform = IssueEditForm()

    return render(
        request,
        'editissue.html',
        {
            'form': editform,
            'nolook': nolook,
        }
    )

@login_required
def edit_issue(request, id):
    issue = get_object_or_404(Issue, pk = id)

    if request.method == "POST":
        editform = IssueEditForm(request.POST, request.FILES, instance=issue)
        if editform.is_valid():
            editform.save()
            if issue.goodcount > issue.count:
                return redirect(issue.get_absolute_url('look'))
            return redirect(issue.get_absolute_url())
    elif request.method == "GET":
        editform = IssueEditForm(instance=issue)

    return render(
        request,
        'editissue.html',
        {
            'form': editform,
            'created_at': issue.datetime,
            'id': id,
            'count': issue.count,
            'goodcount': issue.goodcount,
        }
    )

@user_passes_test(lambda u: u.is_superuser)
def delete_issue(request, id):
    issue = get_object_or_404(Issue, pk = id)
    issue.delete()

    return redirect(issue.get_absolute_url())

def thumb_down(request, id):
    issue = get_object_or_404(Issue, pk = id)

    claimusers = issue.claimusers.split(',')
    ip = get_ipaddress(request)
    if ip not in claimusers:
        issue.claimusers += "," + ip
        issue.count += 1
        issue.save()
    return HttpResponse(status=204)

def thumb_up(request, id):
    issue = get_object_or_404(Issue, pk = id)

    claimusers = issue.claimusers.split(',')
    ip = get_ipaddress(request)
    if ip not in claimusers:
        issue.claimusers += "," + ip
        issue.goodcount += 1
        issue.save()
    return HttpResponse(status=204)

@csrf_exempt
def api_issue(request):
    if request.method == 'GET':
        issues = Issue.objects.all()
        serializer = IssueSerializer(issues, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['claimusers'] = get_ipaddress(request)
        serializer = IssueSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            if request.POST['nolook'] == u'true':
                count = serializer.data['count']
            else:
                count = serializer.data['goodcount']
            return JsonResponse([count,], safe=False, status=201)
        return JsonResponse(serializer.errors, status=400)

def getKey(item):
    return item[1]

def ranking(request, nolook='nolook'):
    startdate = timezone.now() - timezone.timedelta(days=settings.RANKING_DATE_DELTA)
    enddate = timezone.now()
    if nolook == 'nolook':
        issues = Issue.objects.filter(count__gte=1).exclude(email__iexact='').filter(datetime__range=(startdate, enddate)).order_by('email', '-count').select_related('email', 'count')
    else:
        issues = Issue.objects.filter(goodcount__gte=1).exclude(email__iexact='').filter(datetime__range=(startdate, enddate)).order_by('email', '-goodcount').select_related('email', 'goodcount')
    emails = issues.distinct('email').values_list('email', flat=True)

    countList = []

    for email in emails:
        if nolook == 'nolook':
            count = issues.filter(email__iexact=email).aggregate(total_count=Sum('count'))
        else:
            count = issues.filter(email__iexact=email).aggregate(total_count=Sum('goodcount'))
        giza = Giza.objects.filter(email__iexact=email)
        if giza.exists():
            countList.append((giza[0], count['total_count']))

    listRank = sorted(countList, key=getKey, reverse=True)[0:settings.RANKING_LIST_LIMIT]

    template = "ranking.html"
    if is_mobile(request):
        template = "m-ranking.html"

    return render(
        request,
        template,
        {
            'lists': listRank,
            'nolook': nolook,
        }
    )

def rank_archive(request, year, month, nolook='nolook'):
    inyear = int(year)
    inmonth = int(month)
    if inmonth > 0 and inmonth <= 12:
        now = timezone.now()
        startdate = now.replace(year=inyear, month=inmonth, day=1, hour=0, minute=0, second=0, microsecond=0)
        enddate = startdate.replace(month=inmonth+1)

        if nolook == 'nolook':
            issues = Issue.objects.filter(count__gte=1).exclude(email__iexact='').filter(datetime__range=(startdate, enddate)).order_by('email', '-count').select_related('email', 'count')
        else:
            issues = Issue.objects.filter(goodcount__gte=1).exclude(email__iexact='').filter(datetime__range=(startdate, enddate)).order_by('email', '-goodcount').select_related('email', 'goodcount')
        emails = issues.distinct('email').values_list('email', flat=True)

        countList = []

        for email in emails:
            if nolook == 'nolook':
                count = issues.filter(email__iexact=email).aggregate(total_count=Sum('count'))
            else:
                count = issues.filter(email__iexact=email).aggregate(total_count=Sum('goodcount'))
            giza = Giza.objects.filter(email__iexact=email)
            if giza.exists():
                countList.append((giza[0], count['total_count']))

        listRank = sorted(countList, key=getKey, reverse=True)[0:settings.RANKING_LIST_LIMIT]

        if nolook == 'nolook':
            nolookmsg = u'나빠요!'
        else:
            nolookmsg = u'좋아요!'

        msg = u'%s년 %s월 %s를 가장 많이 받은 기자들의 순위입니다.' % (year, month, nolookmsg)

        template = "ranking.html"
        if is_mobile(request):
            template = "m-ranking.html"

        return render(
            request,
            template,
            {
                'lists': listRank,
                'nolook': nolook,
                'msg': msg,
            }
        )
    else:
        return HttpResponse(u"기간 설정 오류")
