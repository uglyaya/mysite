"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from hooked_server import views as hooked_server_views
import xadmin,smart_selects
xadmin.autodiscover();
from xadmin.plugins import xversion
from hooked_server import views 
xversion.register_models()
import django.contrib.auth
urlpatterns = [ 
#     url(r'^admin/', include(admin.site.urls)),
    url(r'^xadmin/', include(xadmin.site.urls)), 
    url(r'^chaining/', include('smart_selects.urls')), 
    url(r'^xadmin/hooked_server/bookgenre/(.+)/import_book/$', views.import_book),
    
    url(r'^genre_list', views.genre_list),
    url(r'^book_list', views.book_list),
    url(r'^book_detail', views.book_detail),
    url(r'^user_token', views.user_token),
    url(r'^user_readlog', views.user_readlog),
    url(r'^language_list', views.language_list),
    
    url(r'^$', hooked_server_views.index),
    url(r'^form/$', hooked_server_views.form),
    url(r'^add/$', hooked_server_views.add),
    url(r'^getjson/(\d+)/(\d+)/$', hooked_server_views.getjson),
    url(r'^jiafa/(\d+)/(\d+)/$', hooked_server_views.jiafa ,name ='add'),
    url(r'^add/(\d+)/(\d+)/$', hooked_server_views.add2 ,name ='add'),    
]
