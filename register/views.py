from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django import forms
from django.utils.http import urlunquote
from .models import *
from datetime import datetime, date, timedelta
#from mainpage.models import Galery

def add_schedule_2x2():
    stylists = Stylist.objects.all()
    for worker in stylists:
        if worker.work_style == 2:
            end_date = WorkSchedule.objects.filter(stylist = worker.pk).order_by('-day_of_work').first().day_of_work
            if end_date > date.today() + timedelta(days=7):
                return
            end_date = end_date - timedelta(days=1)
            q = WorkSchedule.objects.filter(stylist = worker.pk).filter(day_of_work__gte = end_date)
            #выбираем даты большие предпоследней в записи, чтобы на сонове двух последних записанных днях делть вывод о следующем дне
            if q[1].is_work == q[0].is_work == True:
                new_work_schedule = WorkSchedule(stylist = Stylist(id = worker.pk),
                    day_of_work = q[1].day_of_work + timedelta(days=1), is_work = False)
            elif q[1].is_work == q[0].is_work == False:
                new_work_schedule = WorkSchedule(stylist = Stylist(id = worker.pk),
                    day_of_work = q[1].day_of_work + timedelta(days=1), is_work = True)
            else:
                new_work_schedule = WorkSchedule(stylist = Stylist(id = worker.pk),
                    day_of_work = q[1].day_of_work + timedelta(days=1), is_work = q[1].is_work)
            new_work_schedule.save()

def add_blocks():
    end_date = WorkSchedule.objects.order_by('-day_of_work').first().day_of_work
    if end_date > date.today() + timedelta(days=7):
        return
    if not Blocks.objects.order_by('-date').first():
        begin_date = date.today()
    else:
        begin_date = Blocks.objects.order_by('-date').first().date

    times = Times.objects.all()
    stylists = Stylist.objects.all()
    if begin_date is None or begin_date < date.today():
        begin_date = date.today()
    if end_date is None or end_date < date.today():
        end_date = date.today()
    while begin_date != end_date:
        begin_date+= timedelta(days=1)
        for worker in stylists:
            q = WorkSchedule.objects.filter(stylist = worker.pk).filter(day_of_work = begin_date)
            if q[0].is_work:
                for time in times:
                    Blocks.objects.create(time_id=time.id, date=begin_date, stylist=worker)


def register_start(request):
    if request.method == 'POST':
        add_schedule_2x2()
        str = request.POST.get("test")
    return render(request, "register.html")

def functions(request):
    if request.method == 'POST':
        if request.POST["passwd"] == "123":
            return redirect('proxy_func')
    return render(request, 'functions.html')

def proxy_func(request):
    try:
        url = request.META['HTTP_REFERER']
    except Exception:
        return redirect('/')
    add_schedule_2x2()
    add_blocks()
    return redirect('success')
def success(request):
    return render(request, "success.html")