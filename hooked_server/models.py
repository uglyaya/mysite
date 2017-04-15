# -*- coding: UTF-8 -*-
from django.db import models 
from django.db.models.fields import DateField 
from smart_selects.db_fields import ChainedForeignKey 
from mysite import settings
import django.utils.timezone as timezone 
from django.utils.html import format_html
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
def getBookListByGenrecode(genrecode,limit=50):
    if genrecode :
        return Book.objects.filter(genre__code = genrecode)
    else:
        return Book.objects.all()

def getGenreByCode(genrecode):
    return BookGenre.objects.filter(code=genrecode)

def getGenres():
    return BookGenre.objects.all()

def getDetailsByEpisodeid(episodeid):
    return BookDetail.objects.filter(episode__id = episodeid)

def getEpisodeById(episodeid):
    return BookEpisode.objects.get(id=episodeid)

def getAuthorByContact(contact):
    return BookAuthor.objects.get(contact = contact)
##############################
class BookTag(models.Model):
    name = models.CharField(max_length=50) 
    def __unicode__(self):# 在Python3中用 __str__ 代替 __unicode__
        return self.name
        
class BookAuthor(models.Model):
    name = models.CharField(u'作者名',max_length=30)
    contact = models.CharField(u'联系方式',max_length=100,blank = True) 
    def __unicode__(self):# 在Python3中用 __str__ 代替 __unicode__
        return self.name
    
    
class BookGenre(models.Model):
    code = models.CharField(u'文章类型code',max_length=30)
    name = models.CharField(u'文章类型',max_length=30)
    seq = models.IntegerField(u'排序号') #越大的排越后面
    coverImageFile = models.ImageField(upload_to='photos/genre',blank = True,null=True) 
    def __unicode__(self):# 在Python3中用 __str__ 代替 __unicode__
        return self.name
    def image(self):
        if not self.coverImageFile :
            return ''
        return '<img  src="'+settings.MEDIA_URL+'%s" class="field_img"/>' % self.coverImageFile #class="field_img" 可以显示合适的图片
    image.allow_tags = True #这行不加在list页面只会显示图片地址。不会显示图片

class Book(models.Model):
    name = models.CharField(u'书名',max_length=30)
    author = models.ForeignKey(BookAuthor,related_name = "author_set")
    genre = models.ForeignKey(BookGenre,related_name = "genre_set")
    coverImageFile = models.ImageField(upload_to='photos',blank = True,null=True)   
    backmusicFile = models.FileField(upload_to='musics' ,blank = True,null=True)  
    commentCount = models.IntegerField(u'评价数')
    summary = models.CharField(u'简介',max_length=500,blank = True,null=True)
    ctime = models.DateTimeField(u'添加日期',auto_now = False,auto_now_add=True ) #第一次时间
    utime = models.DateTimeField(u'更新时间',auto_now = True,null=True)  #每次都变更。
    tags = models.ManyToManyField(BookTag,blank = True) 
    operator =  models.CharField(u'操作人',max_length=30,blank = True,null=True) #存储最后操作人id
    
    def image(self):
        return '<img  src="'+settings.MEDIA_URL+'%s" class="field_img"/>' % self.coverImageFile #class="field_img" 可以显示合适的图片

    def music(self):
        if self.backmusicFile :
            return '<audio controls="controls"  src="'+settings.MEDIA_URL+'%s" />'% self.backmusicFile
        else:
            return ''
    
    image.allow_tags = True #这行不加在list页面只会显示图片地址。不会显示图片
    music.allow_tags =True 
    
    def __unicode__(self):
        return self.name
     
    
class BookEpisode(models.Model):
    name = models.CharField(u'章节名',max_length=30)
    seq = models.IntegerField(u'排序号') #越大的排越后面
    book = models.ForeignKey(Book)
    def __unicode__(self):# 在Python3中用 __str__ 代替 __unicode__
        return self.name
    
class BookDetail(models.Model):
    sender = models.CharField(u'sender',max_length=30)
    text = models.CharField(u'text',max_length=500)
    seq = models.IntegerField(u'排序号') #越大的排越后面
    book = models.ForeignKey(Book)
    textImageFile = models.ImageField(upload_to='photos/text',blank = True,null=True)   

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
