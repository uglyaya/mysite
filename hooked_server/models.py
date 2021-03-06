# -*- coding: UTF-8 -*-
from django.db import models  
from smart_selects.db_fields import ChainedForeignKey 
from mysite import settings
import django.utils.timezone as timezone 
from django.utils.html import format_html
import hashlib,time 
from bson.json_util import default
# Create your models here.
#在这里可以创建所有的表格。每个表就是一个class


class Person(models.Model):
    name = models.CharField(u'姓名',max_length=30)
    age = models.IntegerField(u'年龄')
    birthday = models.DateField(u'生日',null=True) # 可为空
    tag = models.TextField(u'标签',null=True)
    ctime = models.DateTimeField(u'添加日期',default = timezone.now) #第一次时间
    utime = models.DateTimeField(u'更新时间',auto_now = True,null=True)  #每次都变更。
    class Meta:
#         db_table ='cccc' #可以修改直接指定一个表明
        verbose_name = '测试per' #小导航标题。http://localhost:8000/xadmin/hooked_server/person/ 可看到区别
        verbose_name_plural = '测试person'  #大标题。
    
    def kk(self):  #用来自定义右侧列表栏外加的内容。
        return format_html('<span style="">自定义 参见models</span>')
    
    def __unicode__(self):# 在Python3中用 __str__ 代替 __unicode__
        return self.name
    
class Author(models.Model):
    name = models.CharField(max_length=50) 
    qq = models.CharField(max_length=10)
    addr = models.TextField()
    email = models.EmailField() 
    
class Article(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author)
    content = models.TextField()
    score = models.IntegerField()  # 文章的打分
    tags = models.ManyToManyField('Tag')

class Tag(models.Model):
    name = models.CharField(max_length=50)
    
####################################
ST_CHOICES = (
    (0, u'正常'),
    (-1, u'删除'),
)

POP_CHOICES = {
    (0,u'否'),
    (1,u'是'),
    }

COUNTRY_CHOICES = (
    (u'zh-Hans', u'中文'),
    (u'ja' , u'日语'),
    (u'en' , u'英语'),
    (u'de' , u'德语'),
    (u'es' , u'西班牙'),
    (u'it' , u'意大利'),
    (u'fr' , u'法语'),
    (u'ko' , u'韩语'),
    (u'pt' , u'葡萄牙'),  
)
#获取同一本书book的后一个内容
def getNextBookDetail(detail): 
    details = BookDetail.objects.filter(id=detail.id)
    if len(details) ==0:
        return None
    detail = details[0]
    result = BookDetail.objects.filter(episode=detail.episode ,id__gt = detail.id).order_by('id') 
    if not result or len(result) ==0:
        return None
    else:
        return result[0]

#获取同一本书book的后一个章节Episode
def getNextEpisode(bookid,episodeid):
    result = BookEpisode.objects.filter(book__id = bookid,id__gt = episodeid).order_by('id') 
    if not result or len(result) ==0:
        return 0,''
    else:
        return result[0].id,result[0].name

def getBookListByGenrecode(genrecode,limit=50):
    if genrecode :
        return Book.objects.filter(genre__code = genrecode).order_by('-id') 
    else:
        return Book.objects.all()
    
def getPopBookListByCountry(country,limit=50):
    return Book.objects.filter(genre__country = country,ispop = 1).order_by('-id')[:limit]


def getGenreByCode(genrecode):
    return BookGenre.objects.filter(code=genrecode)

def getGenres(country):
    return BookGenre.objects.filter(country=country,st=0).order_by('seq')

def getLanguages():
    return BookLanguage.objects.filter(st=0)

def getDetailsByEpisodeid(episodeid):
    return BookDetail.objects.filter(episode__id = episodeid)

def getEpisodeById(episodeid):
    return BookEpisode.objects.get(id=episodeid)

def getAuthorByContact(contact):
    return BookAuthor.objects.get(contact = contact)
##############################
class BookLanguage(models.Model):
    code = models.CharField(u'语音代码',unique=True,max_length=32)
    localname = models.CharField(u'本地语言名',unique=True,max_length=32)
    chinesename = models.CharField(u'中文语言名',unique=True,max_length=32) 
    coverImageFile = models.ImageField(upload_to='photos/genre',blank = True,null=True) 
    coverImagePath = models.CharField(u'图片绝对地址',blank = True,null=True,max_length=500)   
    st = models.IntegerField(u'状态',default=0,choices=ST_CHOICES) #缺省0，删除-1
    def image(self): 
        return '<img  src="%s" class="field_img"/>' % (self.getImageUrl()) #class="field_img" 可以显示合适的图片
 
    def getImageUrl(self):
        imgurl = settings.MEDIA_URL+str(self.coverImageFile) if  self.coverImageFile else ''
        return self.coverImagePath if  self.coverImagePath else imgurl
    
    image.allow_tags = True #这行不加在list页面只会显示图片地址。不会显示图片
    def __unicode__(self):
        return self.code
    
class BookUserInfo(models.Model):
    token =models.CharField(u'用户id',unique=True,max_length=32) # jpush使用。目前是存储jpush上传上来的RegistrationID
    ctime = models.DateTimeField(u'添加日期',auto_now = False,auto_now_add=True ) #第一次时间
    utime = models.DateTimeField(u'更新时间',auto_now = True,null=True)  #每次都变更。
    st = models.IntegerField(u'状态',default=0) #缺省0，删除-1
    partId =models.CharField(u'用户分区id',max_length=2) # 为以后数据库分表，把md5（RegistrationID）截取后2位存储。
#     idfa = models.CharField(u'idfa',unique=False,max_length=32,default='') 
    def __unicode__(self):
        return self.token
#     class Meta:  #可以实现联合索引 
#         unique_together = (('userid', 'partid'),)
    
    #重载save方法
    def save(self, force_insert=False, force_update=False, using=None, 
        update_fields=None):
        self.partId = hashlib.md5(self.token).hexdigest()[-2:]
        return models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

class BookTag(models.Model):
    name = models.CharField(max_length=50) 
    def __unicode__(self):
        return self.name
        
class BookAuthor(models.Model):
    name = models.CharField(u'作者名',max_length=30)
    contact = models.CharField(u'联系方式',max_length=100,blank = True) 
    def __unicode__(self):
        return self.name
        
class BookGenre(models.Model):
    code = models.CharField(u'文章类型code',max_length=30)
    name = models.CharField(u'分类名称',max_length=30)
    seq = models.IntegerField(u'排序号',default=0) #越大的排越后面
    coverImageFile = models.ImageField(upload_to='photos/genre',blank = True,null=True) 
    backColor = models.CharField(u'背景颜色',max_length=10,blank = True, default='0x0000FF')
    fontColor = models.CharField(u'字体颜色',max_length=10,blank = True, default='0xFFFFFF' ,
                                 help_text='分类字体的颜色，采用#FFEEBB这个格式。<a href="http://tool.oschina.net/commons?type=3">色表对照</a>')
    country = models.CharField(u'国家',default='zh',max_length=20,choices=COUNTRY_CHOICES)
    st = models.IntegerField(u'状态',default=0,choices=ST_CHOICES) #缺省0，删除-1
    def __unicode__(self):
        return self.name
    def image(self):
        if not self.coverImageFile :
            return ''            
        return '<img  src="'+settings.MEDIA_URL if not self.coverImageFile.startswith('http') else ''+'%s" class="field_img"/>' % self.coverImageFile #class="field_img" 可以显示合适的图片
    image.allow_tags = True #这行不加在list页面只会显示图片地址。不会显示图片
    
    def import_book(self):
        return format_html('<a href="/xadmin/hooked_server/bookgenre/'+str(self.id)+'/import_book/" target="_blank">导入txt</a>\
        |<a href="/xadmin/hooked_server/bookgenre/'+str(self.id)+'/import_book_strawberry/" target="_blank">导入草莓</a>\
        ')
    
    def books(self):  #用来自定义右侧列表栏外加的内容。
        return format_html('<a href="/xadmin/hooked_server/book/?_p_genre__id__exact='+str(self.id)+'">全部书('+str(len(self.genre_set.all()))+'本)</a>')

class Book(models.Model):
    name = models.CharField(u'书名',max_length=200)
    author = models.ForeignKey(BookAuthor,related_name = "author_set")
    genre = models.ForeignKey(BookGenre,related_name = "genre_set")
    coverImageFile = models.ImageField(upload_to='photos',blank = True,null=True,max_length=500)   
    coverImagePath = models.CharField(u'图片绝对地址',blank = True,null=True,max_length=500)   
    backmusicFile = models.FileField(upload_to='musics' ,blank = True,null=True,max_length=500)  
    backmusicPath = models.CharField(u'声音绝对地址',blank = True,null=True,max_length=500)   
    commentCount = models.IntegerField(u'评价数',default=100)
    summary = models.CharField(u'简介',max_length=2000,blank = True,null=True)
    ctime = models.DateTimeField(u'添加日期',auto_now = False,auto_now_add=True ) #第一次时间
    utime = models.DateTimeField(u'更新时间',auto_now = True,null=True)  #每次都变更。
    tags = models.ManyToManyField(BookTag,blank = True) 
    operator =  models.CharField(u'操作人',max_length=30,blank = True,null=True) #存储最后操作人id
    st = models.IntegerField(u'状态',default=0,choices=ST_CHOICES) #缺省0，删除-1
    outid = models.CharField(u'外部id',max_length=200,blank = True,null=True)
    ispop = models.IntegerField(u'是否推荐',default=0,choices=POP_CHOICES) #0否，1是
    
    def image(self): 
        return '<img  src="%s" class="field_img"/>' % (self.getImageUrl()) #class="field_img" 可以显示合适的图片

    def music(self): 
        return '<audio controls="controls"  src="%s" />'%(self.getMuiscUrl()) 
    
    def allepisode(self):
        return format_html('<a href="/xadmin/hooked_server/bookepisode/?_q_='+str(self.id)+'">全部章节('+str(len(self.episode_set.all()))+'章)</a>')
    
    def getImageUrl(self):
        imgurl = settings.MEDIA_URL+str(self.coverImageFile) if  self.coverImageFile else ''
        return self.coverImagePath if  self.coverImagePath else imgurl
    
    def getMuiscUrl(self):
        musicurl =  settings.MEDIA_URL+str(self.backmusicFile) if  self.backmusicFile else ''
        return self.backmusicPath if  self.backmusicPath else musicurl

    image.allow_tags = True #这行不加在list页面只会显示图片地址。不会显示图片
    music.allow_tags =True 
    
    def __unicode__(self):
        return self.name
     
    
class BookEpisode(models.Model):
    name = models.CharField(u'章节名',max_length=500)
    seq = models.IntegerField(u'排序号') #越大的排越后面
    book = models.ForeignKey(Book, related_name='episode_set')
    st = models.IntegerField(u'状态',default=0,choices=ST_CHOICES) #缺省0，删除-1 
    def alldetail(self):  #用来自定义右侧列表栏外加的内容。
        return format_html('<a href="/xadmin/hooked_server/bookdetail/?_q_='+str(self.id)+'">全部内容</a>')
    def __unicode__(self):# 在Python3中用 __str__ 代替 __unicode__
        return self.name
    
class BookDetail(models.Model):
    sender = models.CharField(u'sender',max_length=200,blank = True,null=True)
    text = models.CharField(u'text',max_length=3000,blank = True,null=True)
    seq = models.IntegerField(u'排序号',default=int(time.time())) #越大的排越后面
    book = models.ForeignKey(Book)
    textImageFile = models.ImageField(upload_to='photos/text',blank = True,null=True)   
    textImagePath = models.CharField(u'图片绝对地址',blank = True,null=True,max_length=500)   
    st = models.IntegerField(u'状态',default=0,choices=ST_CHOICES) #缺省0，删除-1
#     episode = models.ForeignKey(BookEpisode)
    episode = ChainedForeignKey(
        BookEpisode, 
        chained_field="book", 
        chained_model_field="book",
        show_all=False, 
        auto_choose=True,
        sort=True)
    
#     imageFile = models.CharField(u'内容图片',max_length=500)
    def __unicode__(self):# 在Python3中用 __str__ 代替 __unicode__
        return self.sender
    
#  
class BookUserReadlog(models.Model):
    user = models.ForeignKey(BookUserInfo,blank = True,null=True)
    bookdetail = models.ForeignKey(BookDetail,blank = True,null=True)
    utime = models.DateTimeField(u'更新时间',auto_now = True,null=True)  #每次都变更。
    ptime = models.DateTimeField(u'更新时间', blank = True,null=True)  #push time。
    st = models.IntegerField(u'状态',default=0) #缺省0，删除-1
    partId =models.CharField(u'用户分区id',max_length=2) # 为以后数据库分表，把md5（RegistrationID）截取后2位存储。
    def __unicode__(self):
        return self.userId
    def save(self, force_insert=False, force_update=False, using=None, 
        update_fields=None):
        self.partId = hashlib.md5(self.user.token).hexdigest()[-2:]
        return models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

class BookPushLog(models.Model):
    user = models.ForeignKey(BookUserInfo,related_name = "log_set")
    bookdetail = models.ForeignKey(BookDetail,blank = True,null=True)
    ctime = models.DateTimeField(u'添加日期',auto_now = False,auto_now_add=True ) #第一次时间 
    
 
# class Continent(models.Model):
#     name = models.CharField(max_length=255)
#     def __str__(self):
#         return self.name
# 
# class Country(models.Model):
#     continent= models.ForeignKey(Continent)
#     name = models.CharField(max_length=255)
#     def __str__(self):
#         return self.name
# 
# class City(models.Model):
#     continent= models.ForeignKey(Continent)
#     country= ChainedForeignKey(Country, chained_field="continent",  chained_model_field="continent", show_all=False, auto_choose=True, sort=True)
#     name = models.CharField(max_length=255)
#     def __str__(self):
#         return self.name
# 
# class Neighborhood(models.Model):
#     continent= models.ForeignKey(Continent)
#     country= ChainedForeignKey(Country, chained_field="continent",  chained_model_field="continent", show_all=False, auto_choose=True, sort=True)
#     name = models.CharField(max_length=255)
#     city= ChainedForeignKey(City, chained_field="country",  chained_model_field="country", show_all=False, auto_choose=True, sort=True)
#     name = models.CharField(max_length=255)
#     def __str__(self):
#         return self.name
