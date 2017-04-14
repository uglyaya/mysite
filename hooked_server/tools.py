# coding=utf-8
import json
from django.db import models
from django.core.serializers import serialize
from django.db.models.query import QuerySet


class JSONEncoder(json.JSONEncoder):
    """ 继承自simplejson的编码基类，用于处理复杂类型的编码
    """

    def default(self, obj):
        if isinstance(obj, QuerySet):
            """ Queryset实例
            直接使用Django内置的序列化工具进行序列化
            但是如果直接返回serialize('json',obj)
            则在simplejson序列化时会被从当成字符串处理
            则会多出前后的双引号
            因此这里先获得序列化后的对象
            然后再用simplejson反序列化一次
            得到一个标准的字典（dict）对象
            """
            return json.loads(serialize('json', obj))
        if isinstance(obj, models.Model):
            """
            如果传入的是单个对象，区别于QuerySet的就是
            Django不支持序列化单个对象
            因此，首先用单个对象来构造一个只有一个对象的数组
            这是就可以看做是QuerySet对象
            然后此时再用Django来进行序列化
            就如同处理QuerySet一样
            但是由于序列化QuerySet会被'[]'所包围
            因此使用string[1:-1]来去除
            由于序列化QuerySet而带入的'[]'
            """
            return json.loads(serialize('json', [obj])[1:-1])
        if hasattr(obj, 'isoformat'):
            # 处理日期类型
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)
    
    
class MyEncoder(json.JSONEncoder):
    def default(self,obj):
        #convert object to a dict
        d = {}
        d['__class__'] = obj.__class__.__name__
        d['__module__'] = obj.__module__
        d.update(obj.__dict__)
        return d
 
class MyDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self,object_hook=self.dict2object)
    def dict2object(self,d):
        #convert dict to object
        if'__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            class_ = getattr(module,class_name)
            args = dict((key.encode('ascii'), value) for key, value in d.items()) #get args
            inst = class_(**args) #create new instance
        else:
            inst = d
        return inst