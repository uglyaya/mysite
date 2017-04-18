#coding:utf-8
from django.http import HttpResponse
from django.http import JsonResponse 
from django.shortcuts import render
from hooked_server.models import Person
from hooked_server.form import AddForm 
from tools import JSONEncoder
import json
from django.forms.models import model_to_dict 
from django.template.context_processors import request
from models import  getNextEpisodeId,getBookListByGenrecode , getGenreByCode,getGenres,getDetailsByEpisodeid,getEpisodeById,BookUserInfo,saveOrUpdateBookUserReadlog
from models import BookUserReadlog
from mysite import settings

#记录用户的token
#http://127.0.0.1:8000/user_token/?token=113xx
# http://api.hooked.top/user_token/?token=xxxx
def user_token(request): 
    token =request.GET['token'] 
    if not token:
        return JsonResponse('no token', safe=False)
    info = BookUserInfo.objects.filter(userId=token)
    if len (info)==0 :
        BookUserInfo(userId=token).save()
    return JsonResponse('ok', safe=False)

#阅读点记录。
#http://127.0.0.1:8000/user_readlog/?token=113&detailid=1
def user_readlog(request):
    token =request.GET['token'] 
    detailid = request.GET['detailid']
    if not token  or not detailid:
        return JsonResponse('param error', safe=False)
    saveOrUpdateBookUserReadlog(token,detailid)
    return JsonResponse('ok', safe=False)
    pass

#获取书籍分类列表   
#http://127.0.0.1:8000/genre_list/?country=CN
#http://api.hooked.top/genre_list/?country=CN
def genre_list(request):
    country = request.GET.get('country')
    genreSet =list( getGenres(country))
    result = {}
    result['count'] = len(genreSet)
    genrelist = []
    for genre in genreSet :
        genrelist.append({ 
            'code':genre.code,
            'name':genre.name,
            'seq':genre.seq,
            'country':genre.country,
            'coverImageFile': settings.MEDIA_URL + str(genre.coverImageFile) if genre.coverImageFile else '',
            'fontColor':genre.fontColor,
            'backColor':genre.backColor,
            })
    result['genres'] = genrelist
    return JsonResponse(result, safe=False)
    
#根据一个分类的code获取书的列表  
# http://127.0.0.1:8000/book_list/?genrecode=aiqing
# http://api.hooked.top/book_list/?genrecode=aiqing
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
            'summary':book.summary,
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
    result['books'] = bookresult
    return JsonResponse(result, safe=False)

# http://127.0.0.1:8000/book_detail/?episodeid=1
# http://api.hooked.top/book_detail/?episodeid=1
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
    result['summary'] = episode.book.summary 
    result['commentCount'] =episode.book.commentCount
    result['coverImageFile'] = settings.MEDIA_URL + str(episode.book.coverImageFile) if episode.book.coverImageFile else ''  
    result['backmusicFile'] =  settings.MEDIA_URL + str(episode.book.backmusicFile) if episode.book.backmusicFile else ''
    nextepisodeid,nextepisodename =getNextEpisodeId(episode.book.id,episodeid)
    result['nextEpisodeid'] = nextepisodeid
    result['nextEpisodename'] = nextepisodename
    for detail in details:
        detailresult.append({
                'id':detail.id,
                'sender':detail.sender,
                'text':detail.text,
                'seq':detail.seq,
                'img':settings.MEDIA_URL + str(detail.textImageFile) if detail.textImageFile else '',
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
