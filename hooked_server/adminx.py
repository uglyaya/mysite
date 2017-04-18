# coding:utf-8
import xadmin
from xadmin import views
from hooked_server.models import Person
# from reversion.models import Revision
from hooked_server.models import Book,BookAuthor,BookDetail,BookEpisode,BookGenre,BookTag
from django.db import models
from form_utils.widgets import ImageWidget
# Register your models here.
 
class PersonAdmin(object):
    list_display=('name','age','birthday','tag','ctime','utime','kk')
    
#保存前执行 其中obj是修改后的对象，form是返回的表单（修改后的），当新建一个对象时 change = False, 当修改一个对象时 change = True
    def save_models(self):
        print 'aaaaaaaaaaaaaaaaaaa'
        obj= self.new_obj
        print self.request.user.email  #这里可以直接访问当前操作的用户信息
        obj.save() 
        
    def delete_models(self):
        print 'delete_model'
#         super().delete_model()
##########################################

#http://www.cnblogs.com/BeginMan/archive/2013/05/11/3072444.html  model额外属性讲解
class BookGenreAdmin(object):
    list_display=('name','image','country','code','seq','books')
    list_filter=('country',)
    ordering = ('seq',) #用作列表页的排序
    pass

class BookAuthorAdmin(object):
    list_display=('name','contact') 
    pass

class BookAdmin(object):
    list_display=('name','allepisode','genre','author','image')
    search_fields=[ 'name','tags__name' ]  #增加一个搜索框
    list_filter=('genre',)
    formfield_overrides = { models.ImageField: {'widget': ImageWidget}}
    
    def save_models(self): 
        obj= self.new_obj
        obj.operator = self.request.user.id  #这里可以直接记录当前操作的用户信息
        obj.save() 

class BookEpisodeAdmin(object):
    list_display=('name','alldetail','book','seq')
    search_fields=[ '=book__id' ]  #增加一个搜索框
    ordering = ('seq',) #用作列表页的排序
    pass

class BookDetailAdmin(object):
    list_display=('sender','text','book','episode','seq')
    search_fields=[ '=episode__id' ]  #增加一个搜索框
    ordering = ('seq',) #用作列表页的排序
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
    menu_style = 'default' #菜单不折叠
#     menu_style =  'accordion' #菜单折叠
     
    apps_label_title = {
        'hooked_server': u'hooked小说',
    }
    
#     def get_nav_menu(self):  
#         menus = super( self).get_nav_menu()  
#        menus.append({  
#            'menus': [{  
#                 'url': '/admin/report',  
#                 'icon': 'search',  
#                 'perm': 'main.view_record',  
#                 'title': '查看班报'  
#            }],  
#            'first_icon': 'calendar',  
#            'title': u'班报查询'  
#        })  
#         return menus
    
    #菜单设置
    def get_site_menu(self): 
        pass
#         print self.admin_site._registry.items()
#         print self.admin_site._registry.items()[1]
        
#         del self.admin_site._registry.items()[1]
#         print len(self.admin_site._registry.items())
        return (
            {'title': 'API接口demo', 'perm': self.get_model_perm(Book, 'view'), 'menus':(
                    {'title': 'genre_list',  'url': '/genre_list/?country=CN' },
                    {'title': 'book_list',  'url': '/book_list/?genrecode=aiqing' },
                    {'title': 'book_detail',  'url': '/book_detail/?episodeid=1' },
                    {'title': 'user_token',  'url': '/user_token/?token=xxxx' },
                    {'title': 'user_readlog',  'url': '/user_readlog/?token=xxxx&detailid=1' }, 
               )}, 
        )
        
#     def get_nav_menu(self):
#         print self.get_site_menu()
    
xadmin.site.register(views.CommAdminView, GlobalSetting)
# xadmin.site.unregister(Revision)

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
