#coding:utf-8
from django import forms
from django.core.validators import RegexValidator

class AddForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()
    c = forms.CharField()
    
#直接上传一本书
class ImportBookForm(forms.Form):
    bookname = forms.CharField(label='书名', required=True)
    author = forms.CharField(label='作者', required=True) 
    summary = forms.CharField(label='简介', required=False,widget=forms.Textarea)
    content =  forms.CharField(label='内容', required=False,widget=forms.Textarea)
    imageurl  =forms.CharField(label='封面地址http', required=False)
#     imagefile = forms.ImageField(label='封面图片文件', required=False)
#     txtfile = forms.FileField(label='Txt文件', required=False,validators=[RegexValidator(r'.+txt$', '请上传txt文件')])
    genreid= forms.CharField(widget = forms.HiddenInput(), required = True)
    
    #从日本no-ichigo.jp网站下载书籍
class ImportBookFormStrawberry(forms.Form):
    bookurl = forms.CharField(label='书首页地址', required=True) 
    imageurl  =forms.CharField(label='封面地址http', required=True) 
    genreid= forms.CharField(widget = forms.HiddenInput(), required = True)