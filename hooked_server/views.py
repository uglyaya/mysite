#coding:utf-8
from django.http import HttpResponse
from django.http import JsonResponse 
from django.shortcuts import render
from hooked_server.models import Person, BookDetail, BookGenre,Book,BookAuthor,BookEpisode
from hooked_server.form import AddForm ,ImportBookForm,ImportBookFormStrawberry
from tools import JSONEncoder
import json
from django.forms.models import model_to_dict 
from django.template.context_processors import request
from models import  getNextEpisode,getBookListByGenrecode , getGenreByCode,getGenres,getDetailsByEpisodeid,getEpisodeById,BookUserInfo,getLanguages
from models import BookUserReadlog
from mysite import settings 
from utils import doget2 

def language_list(request):
    languageSet =list(getLanguages())
    result = {}
    result['count'] = len(languageSet)
    languages = []
    for language in languageSet :
        languages.append({ 
            'code':language.code,
            'localname':language.localname,
            'chinesename':language.chinesename, 
            'imageurl': language.getImageUrl(), 
            })
    result['languages'] = languages
    return JsonResponse(result, safe=False)

#记录用户的token
#http://127.0.0.1:8000/user_token/?token=113xx
# http://api.hooked.top/user_token/?token=xxxx
def user_token(request): 
    token =request.GET['token'] 
    idfa =request.GET['idfa'] 
    if not token:
        return JsonResponse('no token', safe=False)
    userinfo = BookUserInfo.objects.get_or_create(token=token)
    userinfo.idfa =idfa
    userinfo.save()
    return JsonResponse('ok', safe=False)

#阅读点记录。
# http://127.0.0.1:8000/user_readlog/?token=113&detailid=1
def user_readlog(request):
    token =request.GET['token'] 
    detailid = request.GET['detailid']
    if not token  or not detailid or token.find('null')!=-1 or detailid.find('null') !=-1:
        return JsonResponse('param error', safe=False)
    details = BookDetail.objects.filter(id=detailid)
    if len(details) ==0:
        return JsonResponse('detail not exist', safe=False)
    #如果不存在就创建一个
    userinfo,created = BookUserInfo.objects.get_or_create(token=token)
    logs = BookUserReadlog.objects.filter(user__token=token)
    if len(logs) == 0:
        BookUserReadlog(user=userinfo,bookdetail = details[0]).save()
    else:
        log = logs[0]
        log.bookdetail = details[0]
        log.save() 
    return JsonResponse('ok', safe=False)

#获取书籍分类列表   
#http://127.0.0.1:8000/genre_list/?country=zh
#http://api.hooked.top/genre_list/?country=zh
def genre_list(request):
    country = request.GET.get('country')
    if not country :
        country = 'en'
    if len(country.split('-'))>1:
        country = country[0: country.rindex('-')] 
#     country = 'ja'
    genreSet =list(getGenres(country))
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
    if not genrecode:
        return JsonResponse('param error', safe=False)
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
            'coverImageFile': book.getImageUrl(),
            'backmusicFile':   book.getMuiscUrl(),
            'commentCount':book.commentCount,
            'ctime':book.ctime,
            'utime':book.utime,
            'tagscount':book.tags.count(),
            'tags': [model_to_dict(item) for item in book.tags.all() ],
            'episodeCount': len(book.episode_set.all()),
            'episodes': [model_to_dict(item) for item in book.episode_set.all() ], #通过主表获取子表下面的list
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
    nextepisodeid,nextepisodename =getNextEpisode(episode.book.id,episodeid)
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
##########################################
def import_book_strawberry(request,genreid):
    genre = BookGenre.objects.get(id=genreid)
    result = '请添加新书'
    if request.method == 'POST':# 当提交表单时
        form = ImportBookFormStrawberry(request.POST or None, request.FILES or None) # form 包含提交的数据
        if form.is_valid():# 如果提交的数据合法
            bookurl = form.cleaned_data['bookurl'] 
            imageurl = form.cleaned_data['imageurl'] 
            bookidlist =  re.findall(r"(\d+)$",bookurl)
            bookid = bookidlist[0]
            print bookid
            content =doget2(bookurl)
            namelist = re.findall(r'<meta name="title" content="([^\|]+)\|',content)
            bookname = namelist[0].decode()
            print bookname
            authorlist = re.findall(r">([^<]+)</span></a>/著",content)
            authorname = authorlist[0].decode()
            print authorname
            summarylist = re.findall(r'<div id="content-mailcol" class="alignC">(.+)<p class',content, re.S)
            summary = re.sub(r'<[^>]+>', '',summarylist[0].decode())
            summary = re.sub(r'\s','',summary)
            print summary
            author,created = BookAuthor.objects.get_or_create(name = authorname) 
            book,created = Book.objects.get_or_create(
                name=bookname,
                author = author,
                genre = genre,
                commentCount =100,
                summary = summary,
                coverImagePath = imageurl,
                outid = bookid,
                )
            pageslist = re.findall(r"\[(\d+)ページ",content)
            pages = pageslist[0]
            print pages
            content =''
            episodebean = None
            for i in range(int(pages)) :
                url = 'https://no-ichigo.jp/read/page/book_id/%s/page/%s'%(bookid,str(i+1))
                pagecontent = doget2(url)
                chapter = re.findall(r'<p class="chapter">([^<]+)<br />',pagecontent, re.S)
                if chapter and chapter[0]:
                    episodebean ,created = BookEpisode.objects.get_or_create(name=chapter[0].decode(),book=book,seq=i,st=0)   
                elif not episodebean: 
                    episodebean ,created = BookEpisode.objects.get_or_create(name= '第一章',book=book,seq=i,st=0)   
#                 print pagecontent
                page = re.findall(r"<!-- /content-header -->(.+)<!-- /content-mailcol -->",pagecontent, re.S)
                page = re.sub(r'<[^>]+>', '',page[0].decode()) 
#                 print page 
                lines = page.split('\n')
                seq=0
                for line in lines:
                    seq+=1 
                    line = line.strip() 
                    if line !='':
                        print line
                        BookDetail.objects.get_or_create(sender='',text=delEmoji(line),episode=episodebean,book=book,seq=i*10000+seq)
    form = ImportBookFormStrawberry(initial={'genreid': genreid})  #设置表单默认值  
    return  render(request, 'import_book_strawberry.html',{
        'form':form,
        'genre':genre,
        'result':result
        })

#从txt文件导入一本书
def import_book(request,genreid):
    genre = BookGenre.objects.get(id=genreid)
    result = '请添加新书'
    if request.method == 'POST':# 当提交表单时
        form = ImportBookForm(request.POST or None, request.FILES or None) # form 包含提交的数据
        if form.is_valid():# 如果提交的数据合法
            bookname = form.cleaned_data['bookname']
            authorname = form.cleaned_data['author']
            summary = form.cleaned_data['summary']
            genreid = form.cleaned_data['genreid']
            content =form.cleaned_data['content']
            imageurl = form.cleaned_data['imageurl']
#             imagefile=form.cleaned_data['imagefile']
#             txtfile=form.cleaned_data['txtfile']
            author,created = BookAuthor.objects.get_or_create(name = authorname) 
            #保存书
            book,created = Book.objects.get_or_create(
                name=bookname,
                author = author,
                genre = genre,
                commentCount =100,
                summary = summary,
                coverImagePath = imageurl,
                )
            #保存章节
            title = '第一章'
            episodebean ,created = BookEpisode.objects.get_or_create(name=title,book=book,seq=1,st=0)   
            lines = content.split('\n')
            seq=0
            for line in lines:
                seq+=1 
                line = line.strip() 
                print line
#                 line = line.decode('gbk').encode('utf-8')
                if line !='':
                    BookDetail.objects.get_or_create(sender='',text=delEmoji(line),episode=episodebean,book=book,seq=seq)
            result = '**添加成功：'+bookname        
    form = ImportBookForm(initial={'genreid': genreid})  #设置表单默认值  
    return  render(request, 'import_book.html',{
        'form':form,
        'genre':genre,
        'result':result
        })


import re
def delEmoji(str):
    try:
        # Wide UCS-4 build
        myre = re.compile(u'['
            u'\U0001F300-\U0001F64F'
            u'\U0001F600-\U0001F6FF'
            u'\U0001F900-\U0001F9FF'
            u'\u2600-\u2B55]+',
            re.UNICODE)
    except re.error:
        # Narrow UCS-2 build
        myre = re.compile(u'('
            u'\ud83c[\udf00-\udfff]|'
            u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
            u'\ud83e[\udd00-\udfff]|'
            u'[\u2600-\u2B55])+',
            re.UNICODE)
     
    return myre.sub('', str)  # 替换字符串中的Emoji
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
