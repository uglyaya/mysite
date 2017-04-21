#coding:utf-8
from django import forms
from django.core.validators import RegexValidator

class AddForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()
    c = forms.CharField()
    
class ImportBookForm(forms.Form):
    bookname = forms.CharField(label='书名', required=True)
    author = forms.CharField(label='作者', required=True) 
    summary = forms.CharField(label='简介', required=False,widget=forms.Textarea) 
    imagefile = forms.ImageField(label='封面', required=False)
    txtfile = forms.FileField(label='Txt文件', required=False,validators=[RegexValidator(r'.+txt$', '请上传txt文件')])
    genreid= forms.CharField(widget = forms.HiddenInput(), required = True)