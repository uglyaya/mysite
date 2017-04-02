#coding:utf-8
from django.http import HttpResponse
from celery.worker.job import Request
from django.shortcuts import render
 
 
def index(request):
    TutorialList = ["HTML", "CSS", "jQuery", "Python", "Django"]
    dict = {'k1':'v1','k2':'v2'}
    return render(request, 'home.html',{"TutorialList": TutorialList ,'dict':dict })

def add(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a)+int(b)
    return HttpResponse(str(c))


def add2(request,a,b):
    c = int(a)+int(b)
    return HttpResponse(str(c))

def jiafa(request,a,b):
    c = int(a)+int(b)+1
    return HttpResponse(str(c))
