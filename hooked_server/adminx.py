# coding:utf-8
import xadmin
from xadmin import views
from hooked_server.models import Person, Author
from hooked_server.models import Book,BookAuthor,BookDetail,BookEpisode,BookGenre,BookTag
from django.db import models
from form_utils.widgets import ImageWidget
# Register your models here.
 
class PersonAdmin(object):
    list_display=('name','age','birthday','tag','ctime','utime')
##########################################

#http://www.cnblogs.com/BeginMan/archive/2013/05/11/3072444.html  model额外属性讲解
class BookGenreAdmin(object):
    list_display=('name','seq')
    pass

class BookAuthorAdmin(object):
    list_display=('name','contact')
    pass

class BookAdmin(object):
    list_display=('name','genre','author','tags','image','music')
    search_fields=[ 'name','tags__name' ]  #增加一个搜索框
    list_filter=('genre',)
    formfield_overrides = { models.ImageField: {'widget': ImageWidget}}
    pass

class BookEpisodeAdmin(object):
    list_display=('name','book','seq')
    search_fields=[ 'book__name' ]  #增加一个搜索框
    pass

class BookDetailAdmin(object):
    list_display=('sender','text','book','episode','seq')
    search_fields=[ 'book__name' ]  #增加一个搜索框
    pass

class BookTagAdmin(object):
    pass

xadmin.site.register(Person,PersonAdmin) #这些list_display的列需要列在admin里面列出来
xadmin.site.register(BookGenre,BookGenreAdmin) 
xadmin.site.register(Book,BookAdmin) 
xadmin.site.register(BookEpisode,BookEpisodeAdmin) 
xadmin.site.register(BookDetail,BookDetailAdmin) 
xadmin.site.register(BookTag,BookTagAdmin) 
xadmin.site.register(BookAuthor,BookAuthorAdmin) 
 
class GlobalSetting(object):
#     pass
    site_title = 'HOOKED CMS' #修改首页标题
    site_footer = '首页页脚标题'#修改首页页脚标题
    menu_style = 'default'#'accordion'
     
    apps_label_title = {
        'hooked_server': u'hooked小说',
    }
    
    #菜单设置
#     def get_site_menu(self):
#         return (
#             {'title': '投票管理', 'perm': self.get_model_perm(Person, 'view'), 'menus':(
#                    {'title': '投票',  'url': self.get_model_url(Person, 'view')},
#                    {'title':'选票','url': self.get_model_url(Author, 'view')}
#                )},
#         )
    
xadmin.site.register(views.CommAdminView, GlobalSetting)


# from hooked_server.models import City, Continent,Country,Neighborhood
# class ContinentAdmin(object):
#     pass
# class CountryAdmin(object):
#     pass    
# class CityAdmin(object):
#     pass
# class NeighborhoodAdmin(object):
#     pass
# xadmin.site.register(Continent, ContinentAdmin)
# xadmin.site.register(Country, CountryAdmin)
# xadmin.site.register(City, CityAdmin)
# xadmin.site.register(Neighborhood, NeighborhoodAdmin)
