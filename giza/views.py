from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from models import Giza
from giza.forms import GizaEditForm

from django.conf import settings

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

def show_giza(request):
    return render(
        request,
        "showgiza.html",
        {
            'count': 0,
        })

def search_giza(request, searchType, searchWord):
    if searchType == "name":
        db = Giza.objects.filter(name__icontains=searchWord).order_by('belongto')
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
        }
    )
