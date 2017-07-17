# -*- coding: utf-8 -*-
import sys

from core.utils import get_key_1, get_key_2

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.utils import formats, timezone

from giza.models import Giza

from graphos.renderers.gchart import ColumnChart, LineChart, PieChart
from graphos.sources.simple import SimpleDataSource

from issue.forms import IssueEditForm
from models import Issue

reload(sys)
sys.setdefaultencoding('utf-8')


def show_news(request, page=1):
    """Funtion"""
    limit = settings.HOTISSUE_LIMIT
    nextpage = 0
    currentpage = int(page)
    prevpage = currentpage - 1
    startpage = prevpage * limit

    startdate = timezone.now() - timezone.timedelta(days=settings.HOTISSUE_DATE_DELTA)
    enddate = timezone.now()

    total = Issue.objects.filter(datetime__range=(startdate, enddate)).count()

    cut, reminder = divmod(total, limit)
    if reminder > 0:
        cut += 1
    if cut > currentpage:
        nextpage = currentpage + 1

    current_index = startpage + limit
    if current_index > total:
        current_index = total

    issues = Issue.objects.filter(datetime__range=(startdate, enddate)).order_by('-datetime')[startpage:startpage + limit]

    pics = []
    for issue in issues:
        giza = Giza.objects.filter(email__iexact=issue.email)
        if giza.exists():
            pics.append((issue, giza[0].portrait))
        else:
            pics.append((issue, ''))

    template = "issue/showissue.html"

    return render(
        request,
        template,
        {
            'issues': pics,
            'pics': True,
            'nolook': 'all',
            'today': True,
            'currentIndex': current_index,
            'index': page,
            'total': total,
            'prevPage': prevpage,
            'nextPage': nextpage,
            'search_range': 'all',
        }
    )


def new_issue(request, nolook='nolook'):
    """Funtion"""
    if request.method == "POST":
        editform = IssueEditForm(request.POST, request.FILES)
        if editform.is_valid():
            article = editform.save(commit=False)
            try:
                article_check = Issue.objects.filter(url=article.url).get()
                return redirect(article_check.get_absolute_url())
            except ObjectDoesNotExist:
                article.save()
                return redirect(article.get_absolute_url())
    elif request.method == "GET":
        editform = IssueEditForm()

    return render(
        request,
        'issue/editissue.html',
        {
            'form': editform,
            'nolook': nolook,
        }
    )


@login_required
def edit_issue(request, id):
    """Funtion"""
    issue = get_object_or_404(Issue, pk=id)
    referer = ''

    if request.method == "POST":
        editform = IssueEditForm(request.POST, request.FILES, instance=issue)
        if editform.is_valid():
            editform.save()
            nexturl = request.POST['next']
            if nexturl and 'edit' not in nexturl:
                return HttpResponseRedirect(nexturl)
            if issue.goodcount > issue.count:
                return redirect(issue.get_absolute_url('look'))
            return redirect(issue.get_absolute_url())
    elif request.method == "GET":
        editform = IssueEditForm(instance=issue)
        referer = request.META.get('HTTP_REFERER')

    return render(
        request,
        'issue/editissue.html',
        {
            'form': editform,
            'created_at': issue.datetime,
            'id': id,
            'count': issue.count,
            'goodcount': issue.goodcount,
            'next': referer,
        }
    )


@user_passes_test(lambda u: u.is_superuser)
def delete_issue(request, id):
    """Funtion"""
    issue = get_object_or_404(Issue, pk=id)
    issue.delete()

    return redirect(issue.get_absolute_url())


def show_issues(request, nolook='nolook'):
    """Funtion"""
    threshold = settings.BEST_THRESHOLD
    limit = settings.BEST_LIST_LIMIT
    nextpage = 0

    if nolook == 'nolook':
        total = Issue.objects.filter(count__gte=threshold).count()
    else:
        total = Issue.objects.filter(goodcount__gte=threshold).count()

    cut, reminder = divmod(total, limit)
    if (reminder > 0):
        cut += 1
    if (cut > 1):
        nextpage = 2

    current_index = limit
    if current_index > total:
        current_index = total

    if nolook == 'nolook':
        issues = Issue.objects.filter(count__gte=threshold).order_by('-datetime')[0:limit]
    else:
        issues = Issue.objects.filter(goodcount__gte=threshold).order_by('-datetime')[0:limit]

    pics = []
    for issue in issues:

        giza = Giza.objects.filter(email__iexact=issue.email)
        if giza.exists():
            pics.append((issue, giza[0].portrait))
        else:
            pics.append((issue, ''))

    burst_call = False
    if request.user.is_authenticated():
        if request.user.profile.point / settings.BURST_CALL_ACOM >= settings.BURST_CALL_MIN_POINT:
            weekday = timezone.now().weekday()
            if weekday == 4 or weekday == 5:
                burst_call = True

    template = "issue/showissue.html"

    return render(
        request,
        template,
        {
            'issues': pics,
            'pics': True,
            'nolook': nolook,
            'index': 1,
            'currentIndex': current_index,
            'total': total,
            'prevPage': 0,
            'nextPage': nextpage,
            'search_range': 'best',
            'burst_call': burst_call,
        }
    )


def show_best_issues(request, page, nolook='nolook'):
    """Funtion"""
    threshold = settings.BEST_THRESHOLD
    limit = settings.BEST_LIST_LIMIT
    nextpage = 0
    currentpage = int(page)
    prevpage = currentpage - 1
    startpage = prevpage * limit

    if nolook == 'nolook':
        total = Issue.objects.filter(count__gte=threshold).count()
    else:
        total = Issue.objects.filter(goodcount__gte=threshold).count()

    cut, reminder = divmod(total, limit)
    if reminder > 0:
        cut += 1
    if cut > currentpage:
        nextpage = currentpage + 1

    current_index = startpage + limit
    if current_index > total:
        current_index = total

    if nolook == 'nolook':
        issues = Issue.objects.filter(count__gte=threshold).order_by('-datetime')[startpage:startpage + limit]
    else:
        issues = Issue.objects.filter(goodcount__gte=threshold).order_by('-datetime')[startpage:startpage + limit]

    pics = []
    for issue in issues:
        giza = Giza.objects.filter(email__iexact=issue.email)
        if giza.exists():
            pics.append((issue, giza[0].portrait))
        else:
            pics.append((issue, ''))

    burst_call = False
    if request.user.is_authenticated():
        if request.user.profile.point / settings.BURST_CALL_ACOM >= settings.BURST_CALL_MIN_POINT:
            weekday = timezone.now().weekday()
            if weekday == 4 or weekday == 5:
                burst_call = True
        print request.user.profile.point

    template = "issue/showissue.html"

    return render(
        request,
        template,
        {
            'issues': pics,
            'pics': True,
            'nolook': nolook,
            'index': page,
            'currentIndex': current_index,
            'total': total,
            'prevPage': prevpage,
            'nextPage': nextpage,
            'search_range': 'best',
            'burst_call': burst_call,
        }
    )


def search_issue(request, search_range, search_type, search_word, nolook, page=1):
    """Funtion"""
    limit = settings.HOTISSUE_LIMIT
    nextpage = 0
    currentpage = int(page)
    prevpage = currentpage - 1
    startpage = prevpage * limit

    issues = None
    threshold = 1
    total = 0
    today = True
    if search_range == 'best':
        threshold = settings.BEST_THRESHOLD
        today = False

    if nolook == 'all':
        threshold = 0

    if nolook == 'look':
        if search_type == "subject":
            total = Issue.objects.filter(goodcount__gte=threshold).filter(subject__icontains=search_word).count()
            issues = Issue.objects.filter(goodcount__gte=threshold).filter(subject__icontains=search_word).order_by('-datetime')[startpage:startpage + limit]
        elif search_type == "url":
            total = Issue.objects.filter(goodcount__gte=threshold).filter(url__iexact=search_word).count()
            issues = Issue.objects.filter(goodcount__gte=threshold).filter(url__iexact=search_word).order_by('-datetime')[startpage:startpage + limit]
        elif search_type == "email":
            total = Issue.objects.filter(goodcount__gte=threshold).filter(email__icontains=search_word).count()
            issues = Issue.objects.filter(goodcount__gte=threshold).filter(email__icontains=search_word).order_by('-datetime')[startpage:startpage + limit]
        elif search_type == "name":
            giza = Giza.objects.filter(name__iexact=search_word)
            if giza.exists():
                emails = giza.values_list('email', flat=True)
                total = Issue.objects.filter(goodcount__gte=threshold).filter(email__in=emails).count()
                issues = Issue.objects.filter(goodcount__gte=threshold).filter(email__in=emails).order_by('-datetime')[startpage:startpage + limit]
        elif search_type == "belongto":
            giza = Giza.objects.filter(belongto__icontains=search_word)
            if giza.exists():
                emails = giza.values_list('email', flat=True)
                total = Issue.objects.filter(goodcount__gte=threshold).filter(email__in=emails).count()
                issues = Issue.objects.filter(goodcount__gte=threshold).filter(email__in=emails).order_by('-datetime')[startpage:startpage + limit]
    else:
        if search_type == "subject":
            total = Issue.objects.filter(count__gte=threshold).filter(subject__icontains=search_word).count()
            issues = Issue.objects.filter(count__gte=threshold).filter(subject__icontains=search_word).order_by('-datetime')[startpage:startpage + limit]
        elif search_type == "url":
            total = Issue.objects.filter(count__gte=threshold).filter(url__iexact=search_word).count()
            issues = Issue.objects.filter(count__gte=threshold).filter(url__iexact=search_word).order_by('-datetime')[startpage:startpage + limit]
        elif search_type == "email":
            total = Issue.objects.filter(count__gte=threshold).filter(email__icontains=search_word).count()
            issues = Issue.objects.filter(count__gte=threshold).filter(email__icontains=search_word).order_by('-datetime')[startpage:startpage + limit]
        elif search_type == "name":
            giza = Giza.objects.filter(name__iexact=search_word)
            if giza.exists():
                emails = giza.values_list('email', flat=True)
                total = Issue.objects.filter(count__gte=threshold).filter(email__in=emails).count()
                issues = Issue.objects.filter(count__gte=threshold).filter(email__in=emails).order_by('-datetime')[startpage:startpage + limit]
        elif search_type == "belongto":
            giza = Giza.objects.filter(belongto__icontains=search_word)
            if giza.exists():
                emails = giza.values_list('email', flat=True)
                total = Issue.objects.filter(count__gte=threshold).filter(email__in=emails).count()
                issues = Issue.objects.filter(count__gte=threshold).filter(email__in=emails).order_by('-datetime')[startpage:startpage + limit]

    pics = []
    if issues:
        for issue in issues:
            giza = Giza.objects.filter(email__iexact=issue.email)
            if giza.exists():
                pics.append((issue, giza[0].portrait))
            else:
                pics.append((issue, ''))

    template = "issue/showissue.html"

    cut, reminder = divmod(total, limit)
    if reminder > 0:
        cut += 1
    if cut > currentpage:
        nextpage = currentpage + 1

    current_index = startpage + limit
    if current_index > total:
        current_index = total

    return render(
        request,
        template,
        {
            'issues': pics,
            'pics': True,
            'nolook': nolook,
            'search_range': search_range,
            'today': today,
            'index': page,
            'currentIndex': current_index,
            'total': total,
            'prevPage': prevpage,
            'nextPage': nextpage,
            'search_type': search_type,
            'search_word': search_word,
        }
    )


def ranking(request, nolook='nolook', ranktype='default'):
    """Funtion"""
    if ranktype == 'all':
        if nolook == 'nolook':
            issues = Issue.objects.filter(count__gte=1).exclude(email__iexact='').order_by('email', '-count').select_related('email', 'count')
        else:
            issues = Issue.objects.filter(goodcount__gte=1).exclude(email__iexact='').order_by('email', '-goodcount').select_related('email', 'goodcount')
    else:
        startdate = timezone.now() - timezone.timedelta(days=settings.RANKING_DATE_DELTA)
        enddate = timezone.now()
        if nolook == 'nolook':
            issues = Issue.objects.filter(count__gte=1).exclude(email__iexact='').filter(datetime__range=(startdate, enddate)).order_by('email', '-count').select_related('email', 'count')
        else:
            issues = Issue.objects.filter(goodcount__gte=1).exclude(email__iexact='').filter(datetime__range=(startdate, enddate)).order_by('email', '-goodcount').select_related('email', 'goodcount')
    emails = issues.distinct('email').values_list('email', flat=True)

    count_list = []

    for email in emails:
        if nolook == 'nolook':
            count = issues.filter(email__iexact=email).aggregate(total_count=Sum('count'))
        else:
            count = issues.filter(email__iexact=email).aggregate(total_count=Sum('goodcount'))
        giza = Giza.objects.filter(email__iexact=email)
        if giza.exists():
            count_list.append((giza[0], count['total_count']))

    list_rank = sorted(count_list, key=get_key_1, reverse=True)[0:settings.RANKING_LIST_LIMIT]

    if ranktype == 'all':
        if nolook == 'nolook':
            nolookmsg = u'나빠요!'
        else:
            nolookmsg = u'좋아요!'
        msg = u'%s 누적 순위입니다.' % nolookmsg
    else:
        msg = ''

    template = "issue/ranking.html"

    return render(
        request,
        template,
        {
            'lists': list_rank,
            'nolook': nolook,
            'msg': msg,
        }
    )


def rank_archive(request, year, month, nolook, day=0):
    """Funtion"""
    inyear = int(year)
    inmonth = int(month)
    inday = int(day)
    if inmonth > 0 and inmonth <= 12:
        now = timezone.now()
        if inday == 0:
            startdate = now.replace(year=inyear, month=inmonth, day=1, hour=0, minute=0, second=0, microsecond=0)
            enddate = startdate.replace(month=inmonth + 1)
        else:
            enddate = now.replace(year=inyear, month=inmonth, day=inday, hour=0, minute=0, second=0, microsecond=0) - timezone.timedelta(hours=9)
            startdate = enddate - timezone.timedelta(days=7)
            enddate = enddate - timezone.timedelta(microseconds=1)

        if nolook == 'nolook':
            issues = Issue.objects.filter(count__gte=1).exclude(email__iexact='').filter(datetime__range=(startdate, enddate)).order_by('email', '-count').select_related('email', 'count')
        else:
            issues = Issue.objects.filter(goodcount__gte=1).exclude(email__iexact='').filter(datetime__range=(startdate, enddate)).order_by('email', '-goodcount').select_related('email', 'goodcount')
        emails = issues.distinct('email').values_list('email', flat=True)

        count_list = []

        for email in emails:
            if nolook == 'nolook':
                count = issues.filter(email__iexact=email).aggregate(total_count=Sum('count'))
            else:
                count = issues.filter(email__iexact=email).aggregate(total_count=Sum('goodcount'))
            giza = Giza.objects.filter(email__iexact=email)
            if giza.exists():
                count_list.append((giza[0], count['total_count']))

        list_rank = sorted(count_list, key=get_key_1, reverse=True)[0:settings.RANKING_LIST_LIMIT]

        if nolook == 'nolook':
            nolookmsg = u'나빠요!'
        else:
            nolookmsg = u'좋아요!'

        if inday == 0:
            msg = u'%s년 %s월 %s를 가장 많이 받은 기자들의 순위입니다.' % (year, month, nolookmsg)
        else:
            formatted_start = formats.date_format(startdate + timezone.timedelta(hours=9), "Y-m-d")
            formatted_end = formats.date_format(enddate + timezone.timedelta(hours=9), "Y-m-d")
            msg = u'%s ~ %s 사이에 %s를 가장 많이 받은 기자들의 순위입니다.' % (formatted_start, formatted_end, nolookmsg)

        template = "issue/ranking.html"

        return render(
            request,
            template,
            {
                'lists': list_rank,
                'nolook': nolook,
                'msg': msg,
            }
        )
    else:
        return HttpResponse(u"기간 설정 오류")


def chart(request):
    """Funtion"""
    now = timezone.now()

    return chart_archive(request, 'live', now.year, now.month, now.day + 1)


def chart_archive(request, chartfrom, year, month, day=0):
    """Funtion"""
    inyear = int(year)
    inmonth = int(month)
    inday = int(day)
    if inmonth > 0 and inmonth <= 12:
        now = timezone.now()
        if inday == 0:
            startdate = now.replace(year=inyear, month=inmonth, day=1, hour=0, minute=0, second=0, microsecond=0)
            enddate = startdate.replace(month=inmonth + 1)
        else:
            enddate = now.replace(year=inyear, month=inmonth, day=inday, hour=0, minute=0, second=0, microsecond=0) - timezone.timedelta(hours=9)
            startdate = enddate - timezone.timedelta(days=7)
            enddate = enddate - timezone.timedelta(microseconds=1)

        issues = Issue.objects.exclude(email__iexact='').filter(datetime__range=(startdate, enddate)).order_by('count', 'goodcount')

        data_list = [['media', '좋아요', '나빠요']]

        for issue in issues:
            giza = Giza.objects.filter(email__iexact=issue.email)
            if giza:
                found = False
                for item in data_list:
                    if giza[0].belongto == item[0]:
                        item[1] += issue.goodcount
                        item[2] += issue.count
                        found = True
                        break
                if not found:
                    data_list.append([giza[0].belongto, issue.goodcount, issue.count])
                found = False

        data = sorted(data_list, key=get_key_2, reverse=True)[0:settings.RANKING_LIST_LIMIT + 1]
        data_source = SimpleDataSource(data=data)
        chart_all_bad = ColumnChart(data_source)

        data = sorted(data_list, key=get_key_1, reverse=True)[0:settings.RANKING_LIST_LIMIT + 1]
        data_source = SimpleDataSource(data=data)
        chart_all_good = ColumnChart(data_source)

        data = sorted(data_list, key=get_key_1, reverse=True)
        data_source = SimpleDataSource(data=data)
        chart_good = PieChart(data_source)

        data = sorted(data_list, key=get_key_2, reverse=True)
        data_copy = [x[:] for x in data]
        for l in data_copy:
            del l[1]
        data_source = SimpleDataSource(data=data_copy)
        chart_bad = PieChart(data_source)

        trend_data = [['date', data_copy[1][0], data_copy[2][0], data_copy[3][0], data_copy[4][0], data_copy[5][0]]]

        trend_start = startdate
        for i in range(7):
            trend_end = trend_start + timezone.timedelta(1)
            trend_issues = issues.filter(datetime__range=(trend_start, trend_end)).order_by('count', 'goodcount')
            if i == 0:
                trend_data.append([trend_end.date(), 0, 0, 0, 0, 0])
            else:
                trend_data.append([trend_end.date(), trend_data[i][1], trend_data[i][2], trend_data[i][3], trend_data[i][4], trend_data[i][5]])
            for trend_issue in trend_issues:
                giza = Giza.objects.filter(email__iexact=trend_issue.email)
                if giza:
                    for j in range(5):
                        if giza[0].belongto == trend_data[0][j + 1]:
                            trend_data[i + 1][j + 1] += trend_issue.count
            trend_start = trend_end

        data_source = SimpleDataSource(data=trend_data)
        chart_trend = LineChart(data_source)

        if inday == 0:
            msg = u'%s년 %s월 언론사 데이터입니다.' % (year, month)
        elif chartfrom == 'live':
            msg = u'실시간 업데이트되는 일주일간의 언론사 데이터입니다.'
        else:
            formatted_start = formats.date_format(startdate + timezone.timedelta(hours=9), "Y-m-d")
            formatted_end = formats.date_format(enddate + timezone.timedelta(hours=9), "Y-m-d")
            msg = u'%s ~ %s 사이의 언론사 데이터입니다.' % (formatted_start, formatted_end)

        return render(
            request,
            "issue/chart.html",
            {
                'chart_all_bad': chart_all_bad,
                'chart_all_good': chart_all_good,
                'chart_good': chart_good,
                'chart_bad': chart_bad,
                'chart_trend': chart_trend,
                'chartfrom': chartfrom,
                'msg': msg,
            }
        )
    else:
        return HttpResponse(u"기간 설정 오류")
