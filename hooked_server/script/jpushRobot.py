# -*- coding: UTF-8 -*-
'''
Created on 2017年4月19日

@author: zhouc
'''
import sys
reload(sys)
print sys.path
sys.path.append('/home/ec2-user/mysite/')
sys.path.append('/home/ec2-user/mysite/hooked_server/script/')
print sys.path
from mysite import settings
import django,json,datetime,os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
django.setup()
import jpush as jpush
from jpush import common
from hooked_server.models import  getNextBookDetail , BookUserReadlog , BookPushLog


if __name__ == '__main__':
    app_key = '45a4780b0827608a881cb0ad'
    master_secret = 'e61389dff360c1de3cd6861e'
    _jpush = jpush.JPush(app_key, master_secret)
    readlogs = BookUserReadlog.objects.all()
    for readlog in readlogs : 
        nextBookdetail= getNextBookDetail(readlog.bookdetail)
        if not nextBookdetail: continue
        registration_id = readlog.user.token 
        push = _jpush.create_push()
        # if you set the logging level to "DEBUG",it will show the debug logging.
        _jpush.set_logging("WARNING") 
    #     push.audience = jpush.all
        audiences = {'registration_id':[registration_id]}
        push.audience = json.dumps(audiences)
        push.notification = jpush.notification(alert="%s:%s"%(nextBookdetail.sender,nextBookdetail.text))
        push.platform = jpush.all_
        try:
            response=push.send()
            print  response
            readlog.ptime = datetime.datetime.now()
            readlog.save()
            BookPushLog(user=readlog.user,bookdetail=readlog.bookdetail).save()
        except common.Unauthorized:
            raise common.Unauthorized("Unauthorized")
        except common.APIConnectionException:
            raise common.APIConnectionException("conn error")
        except common.JPushFailure:
            print ("JPushFailure")
        except :
            info=sys.exc_info()  
            print info[0],":",info[1]  
            print ("Exception") 