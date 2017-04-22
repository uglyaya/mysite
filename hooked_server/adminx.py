# coding:utf-8
import xadmin
from xadmin import views  
from hooked_server.models import Book,BookAuthor,BookDetail,BookEpisode,BookGenre,BookTag,Person,BookLanguage
from django.db import models
from form_utils.widgets import ImageWidget
from xadmin.plugins.actions import BaseActionView
from django.http import HttpResponse


class MainDashboard(object):
    widgets = [
        [
            {"type": "html", "title": "Test Widget", "content": "<h3> Welcome to Xadmin! </h3><p>Join Online Group: <br/>QQ Qun : 282936295</p>"},
#             {"type": "chart", "model": "app.accessrecord", 'chart': 'user_count', 'params': {'_p_date__gte': '2013-01-08', 'p': 1, '_p_date__lt': '2013-01-29'}},
#             {"type": "list", "model": "app.host", 'params': { 'o':'-guarantee_date'}},
        ],
        [
#             {"type": "qbutton", "title": "Quick Start", "btns": [{'model': Person}, {'model':Author}, {'title': "Google", 'url': "http://www.google.com"}]},
            {"type": "addform", "model": Person}, 
        ]
    ]
xadmin.site.register(views.IndexView, MainDashboard)


class PersonAdmin(object):
    list_display=('name','age','birthday','tag','ctime','utime','kk')
    #重载系统内的模版页面，可以修改为自定义的。
    add_form_template = 'views/form.html'
    change_form_template = 'views/form.html'
    
#保存前执行 其中obj是修改后的对象，form是返回的表单（修改后的），当新建一个对象时 change = False, 当修改一个对象时 change = True
    def save_models(self): 
        obj= self.new_obj
        print self.request.user.email  #这里可以直接访问当前操作的用户信息
        obj.save() 
        
    def delete_models(self):
        print 'delete_model'
#         super().delete_model()
##########################################
# 插件动作Action   ：https://github.com/WBowam/wbowam.github.com/wiki/Xadmin-start(2)  
class BookGenreAction(BaseActionView):
    # 这里需要填写三个属性
    action_name = "bookgenre_action_close"    #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = (u'修改状态 %(verbose_name_plural)s') #: 描述, 出现在 Action 菜单中, 可以使用 ``%(verbose_name_plural)s`` 代替 Model 的名字.
    model_perm = 'change'    #: 该 Action 所需权限
    # 而后实现 do_action 方法
    def do_action(self, queryset):
        # queryset 是包含了已经选择的数据的 queryset
        for obj in queryset:
            # obj 的操作
            print obj
        # 返回 HttpResponse
        return HttpResponse('ok')

#http://www.cnblogs.com/BeginMan/archive/2013/05/11/3072444.html  model额外属性讲解
class BookGenreAdmin(object):
    list_display=('name','books','country','code','seq','image','import_book')
    list_filter=('country',)
    actions = [BookGenreAction, ]  #上面定义的那个action
    list_editable = ['name', ]  #列表页修改。对于价格，状态等参数比较好用。
    ordering = ('seq',) #用作列表页的排序
    pass

class BookAuthorAdmin(object):
    list_display=('name','contact')  

class BookLanguageAdmin(object):
    list_display=('code','localname','chinesename','image')  

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
    list_display=('id','sender','text','book','episode','seq')
    search_fields=[ '=episode__id' ]  #增加一个搜索框
    ordering = ('seq',) #用作列表页的排序
    pass

class BookTagAdmin(object):
    pass

xadmin.site.register(Person,PersonAdmin) #这些list_display的列需要列在admin里面列出来
xadmin.site.register(BookLanguage,BookLanguageAdmin) 
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
        return (
            {'title': 'API接口demo', 'perm': self.get_model_perm(Book, 'view'), 'menus':(
                    {'title': 'language_list',  'url': '/language_list/' },
                    {'title': 'genre_list',  'url': '/genre_list/?country=CN' },
                    {'title': 'book_list',  'url': '/book_list/?genrecode=aiqing' },
                    {'title': 'book_detail',  'url': '/book_detail/?episodeid=1' },
                    {'title': 'user_token',  'url': '/user_token/?token=xxxx' },
                    {'title': 'user_readlog',  'url': '/user_readlog/?token=xxxx&detailid=1' }, 
               )}, 
        ) 
xadmin.site.register(views.CommAdminView, GlobalSetting)


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = False
xadmin.sites.site.register(views.BaseAdminView, BaseSetting)
#
from xpluging import *