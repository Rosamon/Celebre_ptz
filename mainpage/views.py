from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import Galery

def index(request):
    buf_count = Galery.objects.count()
    if buf_count % 3 == 0:
        data = Galery.objects.all()
    elif buf_count % 3 == 1:
        buf_count -= 1
        data = Galery.objects.filter(pk__lt=buf_count)
    elif buf_count % 3 == 2:
        buf_count -= 2
        data = Galery.objects.filter(pk__lt=buf_count)

    return render(request,'index.html',{'data': data, 'count': buf_count})
    #HttpResponse("MAIN")
    

def pageNotFound(request, exception):
    return redirect('mainpage/index.html')
    #HttpResponseNotFound('<h1>Страница не найдена</h1>')