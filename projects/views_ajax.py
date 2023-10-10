from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Project, Schedule
from accounts.models import Structure, OAUser
from django.db.models import Q
from django.db.models import Sum
import json
import datetime

import csv
# Create your views here.


@login_required
def load_projects(request):

    kw = request.GET.get('q', '')
    data = {}
    if kw != '':
        user = request.user
        projects = Project.objects.filter(
            Q(department=user.department), Q(name__contains=kw))
        data["results"] = [{"id": lt.pk, "text": lt.name} for lt in projects]
    data["pagination"] = {"more": True}
    return HttpResponse(json.dumps(data))


def get_tasks_day(uid: int, num: int) -> list:

    taskday = []
    today = datetime.datetime.now()
    user = OAUser.objects.get(pk=uid)
    if not user:
        return taskday

    finret = Schedule.objects.filter(Q(transactor=user),
                                     Q(department=user.department),
                                     Q(isfin=True))
    ret = finret.filter(lcdate__gte=str(today.date())+' 00:00:00')
    taskday.append(len(ret))
    for i in range(1, num):
        cday = (today + datetime.timedelta(days=-i))
        ret = finret.filter(lcdate__gte=str(cday.date())+' 00:00:00',
                            lcdate__lte=str(today.date())+' 23:59:59')
        taskday.append(len(ret))
        today = cday
    taskday.reverse()
    return taskday


@login_required
def load_tasksto_dayfin(request, u_id):
    dstr = request.GET.get('day', '1')
    day = 1
    if dstr.isdigit():
        day = int(dstr)
    else:
        day = 1
    data = {}
    data["series"] = get_tasks_day(u_id, day)
    return HttpResponse(json.dumps(data))


@login_required
def load_tasks_dayfin(request):
    user = request.user
    return load_tasksto_dayfin(request, user.id)

    # dstr = request.GET.get('day', '1')
    # day = 1
    # if dstr.isdigit():
    #     day = int(dstr)
    # else:
    #     day = 1

    # data = {}
    # user = request.user
    # data["series"] = get_tasks_day(user.id,day)
    # return HttpResponse(json.dumps(data))
