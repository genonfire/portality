# -*- coding: utf-8 -*-

import sys

from core.utils import get_media_from_email, month_range

from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.utils import timezone

from forms import GizaEditForm
from models import Giza

reload(sys)
sys.setdefaultencoding('utf-8')


@login_required
def show_all_giza(request):
    """Function"""
    db = Giza.objects.order_by('belongto', 'name').all()
    template = "giza/showgiza.html"

    return render(
        request,
        template,
        {
            'db': db,
            'count': db.count(),
        }
    )


def show_giza(request):
    """Function"""
    now = timezone.now()
    startyear = settings.RANKING_START_YEAR
    startmonth = settings.RANKING_START_MONTH
    nowyear = now.year
    nowmonth = now.month
    month_list = []

    for i in month_range(startmonth, startyear, nowmonth, nowyear):
        month_list.append(i)

    template = "giza/showgiza.html"

    return render(
        request,
        template,
        {
            'count': 0,
            'lists': reversed(month_list),
        })


def search_giza(request, search_type, search_word):
    """Function"""
    word = search_word.rstrip()
    template = "giza/showgiza.html"
    email = ''

    if search_type == "name":
        db = Giza.objects.filter(name__iexact=word).order_by('belongto', 'name')
    elif search_type == "email":
        db = Giza.objects.filter(email__icontains=word).order_by('belongto', 'name')
        if not db.exists():
            email = search_word
    elif search_type == "belongto":
        db = Giza.objects.filter(belongto__icontains=word).order_by('belongto', 'name')
    elif search_type == "twitter":
        db = Giza.objects.filter(twitter__icontains=word).order_by('belongto', 'name')
    elif search_type == "facebook":
        db = Giza.objects.filter(facebook__icontains=word).order_by('belongto', 'name')
    else:
        return render(
            request,
            template,
            {
                'count': 0,
            }
        )

    return render(
        request,
        template,
        {
            'db': db,
            'count': db.count(),
            'email': email,
            'search_type': search_type,
        }
    )


@login_required
def new_giza(request, email=''):
    """Function"""
    if request.method == "POST":
        editform = GizaEditForm(request.POST, request.FILES)
        if editform.is_valid():
            giza = editform.save(commit=False)
            giza.user = request.user
            giza_check = Giza.objects.filter(email__iexact=giza.email)
            if (giza_check):
                return HttpResponse(u"이미 존재합니다.<br><a href='javascript:history.back()''>돌아가기</a>")
            giza.save()
            print giza.get_serach_url(giza.email)
            return redirect(giza.get_serach_url(giza.email))
    elif request.method == "GET":
        editform = GizaEditForm()

    media = get_media_from_email(request, email)

    return render(
        request,
        "giza/editgiza.html",
        {
            'form': editform,
            'edituser': '',
            'email': email,
            'media': media
        }
    )


@login_required
def edit_giza(request, id):
    """Function"""
    giza = get_object_or_404(Giza, pk=id)
    referer = ''

    if request.method == "POST":
        editform = GizaEditForm(request.POST, request.FILES, instance=giza)
        if editform.is_valid():
            giza = editform.save(commit=False)
            giza.user = request.user
            giza.save()
            nexturl = request.POST['next']
            if nexturl and 'edit' not in nexturl:
                return HttpResponseRedirect(nexturl)
            return redirect(giza.get_absolute_url())
    elif request.method == "GET":
        editform = GizaEditForm(instance=giza)
        referer = request.META.get('HTTP_REFERER')

    return render(
        request,
        "giza/editgiza.html",
        {
            'form': editform,
            'edituser': giza.user,
            'id': id,
            'next': referer,
        }
    )


@user_passes_test(lambda u: u.is_superuser)
def delete_giza(request, id):
    """Function"""
    giza = get_object_or_404(Giza, pk=id)
    giza.delete()

    return redirect(giza.get_absolute_url())
