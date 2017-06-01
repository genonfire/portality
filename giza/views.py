#-*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.core.mail import send_mail
from smtplib import SMTPException
from django.core.signing import Signer, TimestampSigner
from django.core.context_processors import csrf
from django.conf import settings

from models import Giza
from giza.forms import GizaEditForm, RegistrationForm

import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def show_all_giza(request):
    db = Giza.objects.order_by('belongto').all()

    return render(
        request,
        "showgiza.html",
        {
            'db': db,
            'count': db.count(),
        }
    )

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timezone.timedelta(n)

def month_range(startmonth, startyear, endmonth, endyear ):
    rangeStart = startyear * 12 + startmonth - 1
    rangeEnd = endyear * 12 + endmonth - 1
    for i in range(rangeStart, rangeEnd):
        y, m = divmod(i, 12)
        yield y, m + 1

def show_giza(request):
    now = timezone.now()
    startyear = settings.RANKING_START_YEAR
    startmonth = settings.RANKING_START_MONTH
    nowyear = now.year
    nowmonth = now.month
    monthList = []

    for i in month_range(startmonth, startyear, nowmonth, nowyear):
        monthList.append(i)

    return render(
        request,
        "showgiza.html",
        {
            'count': 0,
            'lists': reversed(monthList),
        })

def search_giza(request, searchType, searchWord):
    if searchType == "name":
        db = Giza.objects.filter(name__iexact=searchWord).order_by('belongto')
    elif searchType == "email":
        db = Giza.objects.filter(email__icontains=searchWord).order_by('belongto')
    elif searchType == "belongto":
        db = Giza.objects.filter(belongto__icontains=searchWord).order_by('belongto')
    elif searchType == "twitter":
        db = Giza.objects.filter(twitter__icontains=searchWord).order_by('belongto')
    elif searchType == "facebook":
        db = Giza.objects.filter(facebook__icontains=searchWord).order_by('belongto')
    else:
        return render(
            request,
            "showgiza.html",
            {
                'count': 0,
            }
        )

    return render(
        request,
        "showgiza.html",
        {
            'db': db,
            'count': db.count(),
        }
    )

@login_required
def new_giza(request):
    if request.method == "POST":
        editform = GizaEditForm(request.POST, request.FILES)
        if editform.is_valid():
            giza = editform.save(commit=False)
            giza.user = request.user
            gizaCheck = Giza.objects.filter(email__iexact=giza.email)
            if (gizaCheck):
                return HttpResponse(u"이미 존재합니다.<br><a href='javascript:history.back()''>돌아가기</a>")
            giza.save()
            return redirect(giza.get_absolute_url())
    elif request.method == "GET":
        editform = GizaEditForm()

    return render(
        request,
        "editgiza.html",
        {
            'form': editform,
            'edituser': ''
        }
    )

@login_required
def edit_giza(request, id):
    giza = get_object_or_404(Giza, pk = id)

    if request.method == "POST":
        editform = GizaEditForm(request.POST, request.FILES, instance=giza)
        if editform.is_valid():
            giza = editform.save(commit=False)
            giza.user = request.user
            giza.save()
            return redirect(giza.get_absolute_url())
    elif request.method == "GET":
        editform = GizaEditForm(instance=giza)

    return render(
        request,
        "editgiza.html",
        {
            'form': editform,
            'edituser': giza.user,
            'id': id,
        }
    )

@user_passes_test(lambda u: u.is_superuser)
def delete_giza(request, id):
    giza = get_object_or_404(Giza, pk = id)
    giza.delete()

    return redirect(giza.get_absolute_url())

def check_validation(request):
    username = request.POST.get('username')
    idcheck = User.objects.filter(username__iexact=username).exists()

    code = request.POST.get('code')
    email = request.POST.get('email')
    signer = TimestampSigner()
    msg = ''
    result = False

    try:
        value = signer.unsign(code, max_age=180)
        codeCheck = value == email

        if idcheck:
            msg = u"이미 존재하는 아이디입니다."
        elif not codeCheck:
            msg = u"인증코드가 잘못되었습니다."
        else:
            result = True
    except:
        msg = u"인증코드가 잘못되었습니다."

    data = {
        'result': result,
        'msg': msg,
    }

    return JsonResponse(data)

def sign_up(request):
    if request.method == "POST":
        userform = RegistrationForm(request.POST)
        if userform.is_valid():
            userform.save(commit=False)
            email = userform.cleaned_data['email']
            code = userform.cleaned_data['code']
            signer = TimestampSigner()
            try:
                value = signer.unsign(code, max_age=180)
                idCheck = value == email
                if (idCheck):
                    msg = u"가입성공.<br><a href=%s>로그인</a>" % reverse_lazy('login')
                    userform.save()
                else:
                    msg = u"인증코드를 확인해 주세요."
            except:
                msg = u"인증코드를 확인해 주세요.."
        else:
            msg = u"회원가입 오류.<br>아이디를 확인해 주세요."
        return HttpResponse(msg)
    elif request.method == "GET":
        userform = RegistrationForm()

    return render(
        request,
        "signup.html",
        {
            'userform': userform,
        }
    )

def check_duplication(request):
    username = request.POST.get('username')
    idcheck = User.objects.filter(username__iexact=username).exists()
    if (idcheck):
        msg = u"이미 존재하는 아이디입니다."
    else:
        msg = u"사용 가능한 아이디입니다."
    data = {
        'idcheck': idcheck,
        'msg': msg,
    }
    return JsonResponse(data)

def check_email(request):
    id_email = request.POST.get('email')
    signer = TimestampSigner()
    value = signer.sign(id_email)
    subject = u'[gencode.me] 회원가입 인증 메일입니다.'
    body = u'인증코드(이메일주소 포함): %s' % value

    try:
        send_mail(subject, body, settings.EMAIL_HOST_USER, [id_email], fail_silently=False)
        return HttpResponse(status=201)
    except SMTPException:
        return HttpResponse(status=400)

@user_passes_test(lambda u: u.is_superuser)
def send_email(request):
    id_email = request.user.email
    print "sending email to", id_email
    signer = TimestampSigner()
    value = signer.sign(id_email)
    subject = u'[gencode.me] 테스트 메일입니다.'
    body = u'인증코드(이메일주소 포함): %s' % value

    try:
        send_mail(subject, body, settings.EMAIL_HOST_USER, [id_email], fail_silently=False)
        return HttpResponse("email sent", status=201)
    except SMTPException:
        return HttpResponse(status=400)
