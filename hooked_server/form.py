#coding:utf-8
from django import forms
 
class AddForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()
    c = forms.CharField()