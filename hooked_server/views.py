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
from django.template.context_processors import request
from models import getBookListByGenrecode , getGenreByCode,getGenres,getDetailsByEpisodeid,getEpisodeById
from mysite import settings

#获取书籍分类列表   http://127.0.0.1:8000/genre_list/
def genre_list(request):
    genreSet =list( getGenres())
    result = {}
    result['count'] = len(genreSet)
    genrelist = []
    for genre in genreSet :
        genrelist.append({ 'code':genre.code,'name':genre.name})
    result['genres'] = genrelist
    return JsonResponse(result, safe=False)
    
#根据一个分类的code获取书的列表  http://127.0.0.1:8000/book_list/?genrecode=yq
def book_list(request):  
    genrecode = request.GET.get('genrecode')
    genreSet = getGenreByCode(genrecode)
    if not genreSet :
        return JsonResponse('genre error', safe=False)
    bookresult = []
    books = list(getBookListByGenrecode(genrecode))
    for book in books:
        bookresult.append({
            'id':book.id,
            'name':book.name,
            'author':book.author.name,
            'genre':book.genre.name,
            'coverImageFile': settings.MEDIA_URL + str(book.coverImageFile) if book.coverImageFile else '',
            'backmusicFile':   settings.MEDIA_URL + str(book.backmusicFile) if book.backmusicFile else '',
            'commentCount':book.commentCount,
            'ctime':book.ctime,
            'utime':book.utime,
            'tagscount':book.tags.count(),
            'tags': [model_to_dict(item) for item in book.tags.all() ],
            'episodeCount': len(book.bookepisode_set.all()),
            'episodes': [model_to_dict(item) for item in book.bookepisode_set.all() ], #通过主表获取子表下面的list
            })
    genre = genreSet[0]
    result ={} 
    result['genrecode'] = genrecode
    result['genrename'] = genre.name
    result['bookcount'] = len(books)
    result['bookresult'] = bookresult
    return JsonResponse(result, safe=False)

#http://127.0.0.1:8000/book_detail/?episodeid=1
def book_detail(request):
    episodeid = request.GET.get('episodeid')
    episode = getEpisodeById(episodeid)
    details = getDetailsByEpisodeid(episodeid)
    result ={} 
    detailresult =[]
    result['episodeid'] =episodeid
    result['episodename'] =episode.name
    result['bookid'] =episode.book.id
    result['bookname'] =episode.book.name 
    result['detailcount'] =len(details)
    result['authorid'] = episode.book.author.id
    result['authorname'] = episode.book.author.name
    result['commentCount'] =episode.book.commentCount
    result['coverImageFile'] = settings.MEDIA_URL + str(episode.book.coverImageFile) if episode.book.coverImageFile else ''  
    result['backmusicFile'] =  settings.MEDIA_URL + str(episode.book.backmusicFile) if episode.book.backmusicFile else '' 
    for detail in details:
        detailresult.append({
                'id':detail.id,
                'sender':detail.sender,
                'text':detail.text,
                'seq':detail.seq,
            })
    result['details'] =detailresult
    return JsonResponse(result, safe=False)



###########################################
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
#     person = Person.objects.get(id=1);
#     c['one'] = model_to_dict(person);
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
