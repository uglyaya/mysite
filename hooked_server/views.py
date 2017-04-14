#coding:utf-8
from django.http import HttpResponse
from django.http import JsonResponse 
from django.shortcuts import render
from hooked_server.models import Person
from hooked_server.form import AddForm
from django.core import serializers
from tools import JSONEncoder
import json
from django.forms.models import model_to_dict

def index(request):
    TutorialList = ["HTML", "CSS", "jQuery", "Python", "Django"]
    dict = {'k1':'v1','k2':'v2'}
    return render(request, 'home.html',{"TutorialList": TutorialList ,'dict':dict ,'person': Person.objects.get(id='1')})

#直接在url里面通过&方式链接参数的写法
def add(request):
    a = request.GET['a']
    b = request.GET['b']
    c = int(a)+int(b)
    return HttpResponse(str(c))

#优雅的在url里面用/分割传递参数的写法
def add2(request,a,b):
    c = int(a)+int(b)
    return HttpResponse(str(c))

#通过json方式返回结果
def getjson(request,a,b):
    c = {};
    c['a'] = int(a);
    c['b'] = b;
    person = Person.objects.get(id=1);
    c['one'] = model_to_dict(person);
    persons = Person.objects.all();
    all = [];
    for p in persons :
        all.append( {'name': p.name,'age': p.age} );
    c['all'] = all;
#     c['persions'] = repr( persons); 
    print json.dumps(c);
    cc = json.loads(str(json.dumps(c)));
    print str(cc);
    return HttpResponse(json.dumps(cc, cls=JSONEncoder))

def jiafa(request,a,b):
    c = int(a)+int(b)+1
    return HttpResponse(str(c))

def form(request):
    if request.method == 'POST':# 当提交表单时
        form = AddForm(request.POST) # form 包含提交的数据
        if form.is_valid():# 如果提交的数据合法
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return HttpResponse(str(int(a) + int(b)))
    else:# 当正常访问时
        form = AddForm()
    return render(request, 'form.html', {'form': form})
