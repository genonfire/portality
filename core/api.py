# -*- coding: utf-8 -*-
import sys

from core.utils import get_ipaddress

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from issue.models import Issue
from issue.serializers import IssueSerializer

reload(sys)
sys.setdefaultencoding('utf-8')


def api_vote(request, liketype='dislike'):
    """API vote"""
    if request.method == 'POST':
        issue_id = request.POST['id']
        ip = get_ipaddress(request)
        issue = get_object_or_404(Issue, pk=issue_id)
        claimusers = issue.claimusers.split(',')

        if ip not in claimusers:
            issue.claimusers += "," + ip
            if liketype == 'like':
                issue.goodcount += 1
            else:
                issue.count += 1
            issue.save()

            if request.user.is_authenticated():
                if request.user.profile.point < settings.POINT_MAX:
                    now = timezone.now()
                    if issue.datetime > now - timezone.timedelta(days=7):
                        request.user.profile.point += 1
                        request.user.profile.save()

            if liketype == 'like':
                return JsonResponse([issue.goodcount], safe=False, status=201)
            else:
                return JsonResponse([issue.count], safe=False, status=201)
        else:
            return JsonResponse({'status': 'false'}, status=400)
    else:
        return JsonResponse({'status': 'false'}, status=400)


def api_burst_call(request):
    """API burst call"""
    if request.method == 'POST':
        if request.user.is_authenticated():
            now = timezone.now()
            lastcall = request.user.profile.lastcall
            if now - timezone.timedelta(days=5) > lastcall:
                if now.weekday() == 4 or now.weekday() == 5:
                    issue_id = request.POST['id']
                    nolook = request.POST['nolook']
                    issue = get_object_or_404(Issue, pk=issue_id)
                    point = request.user.profile.point / settings.BURST_CALL_ACOM

                    if point >= settings.BURST_CALL_MIN_POINT:
                        if nolook == 'nolook':
                            issue.count += point
                            count = issue.count
                        else:
                            issue.goodcount += point
                            count = issue.goodcount

                        issue.save()
                        request.user.profile.point = 0
                        request.user.profile.lastcall = timezone.now()
                        request.user.profile.save()

                        return JsonResponse([count], safe=False, status=201)
                else:
                    return JsonResponse([0], safe=False, status=201)
            else:
                return JsonResponse([0], safe=False, status=201)
    return JsonResponse({'status': 'false'}, status=400)


@csrf_exempt
def api_issue(request):
    """API for chrome extension"""
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
            return JsonResponse([count, ], safe=False, status=201)
        return JsonResponse(serializer.errors, status=400)
