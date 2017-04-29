# -*- coding: UTF-8 -*-
'''
Created on 2017年4月17日

@author: zhouc
'''
import django,urllib2,json,urllib ,sys
import requests 
from wsgiref import headers

def doget2(url):
    response = urllib2.urlopen(url)
    return  response.read()

def doget(url):
    _USER_AGENT = "Mozilla/5.0 (Linux; U; Android 4.0.4; zh-cn; MI-ONE Plus Build/IMM76D) AppleWebKit/533.1 (KHTML, like Gecko)Version/4.0 MQQBrowser/4.4 Mobile Safari/533.1";
    httphandler = urllib2.HTTPHandler(debuglevel=0);
    opener = urllib2.build_opener(httphandler);
    headers = {"user-agent": _USER_AGENT};
    req = urllib2.Request(url, headers=headers);
    f = opener.open(req, timeout=20);
 
    if f.getcode() == 200: 
        if f.geturl() == url :
            content = f.read();
            return content
        else:
            print "302:"+f.geturl()
            
def dopost(url,body,headers):    
    req = urllib2.Request(url, body)       # 生成页面请求的完整数据
    req.add_header('User-Agent', 'HOOKED/153 CFNetwork/758.5.3 Darwin/15.6.0')
    req.add_header('X-Parse-Application-Id', 'Vh382DiUoSheUIWSKkhhH7UV2e8KXeg0wtWh3W1i')
    req.add_header('X-Parse-Client-Key', 'V9BdkdFFzHqxb7he0uEy05vdC7CXsfVUmg6Raxik')
    req.add_header('X-Parse-Session-Token', 'r:b58226bca9ee82b2e67e55eaec6a66d3')
#     req.add_header('', '')
     
    response = urllib2.urlopen(req)       # 发送页面请求
    return response.read()                    # 获取服务器返回的页面信息


import re
def delEmoji(str):
    try:
        # Wide UCS-4 build
        myre = re.compile(u'['
            u'\U0001F300-\U0001F64F'
            u'\U0001F600-\U0001F6FF'
            u'\U0001F900-\U0001F9FF'
            u'\u2600-\u2B55]+',
            re.UNICODE)
    except re.error:
        # Narrow UCS-2 build
        myre = re.compile(u'('
            u'\ud83c[\udf00-\udfff]|'
            u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
            u'\ud83e[\udd00-\udfff]|'
            u'[\u2600-\u2B55])+',
            re.UNICODE)
     
    return myre.sub('', str)  # 替换字符串中的Emoji

if __name__ == '__main__':
#     print dopost('https://production.hooked.media/parse/functions/retrieveUnreadStories', '{"genre":{"variant":0,"genreUID":"Romance"},"includeStoryKeyPaths":["author"]}')
    headers = {
        'User-Agent': 'HOOKED/153 CFNetwork/758.5.3 Darwin/15.6.0',
        'X-Parse-Application-Id':'Vh382DiUoSheUIWSKkhhH7UV2e8KXeg0wtWh3W1i',
        'X-Parse-Client-Key': 'V9BdkdFFzHqxb7he0uEy05vdC7CXsfVUmg6Raxik',
        'X-Parse-Session-Token': 'r:b58226bca9ee82b2e67e55eaec6a66d3',
        'X-Parse-Installation-Id': 'ebed561e-8fbd-4f56-814d-bf481ec2a496',
        'Content-Type':'application/json; charset=utf-8',
        'X-Parse-Client-Version':'i1.14.2',
        'X-Parse-OS-Version':'9.3.5 (13G36)',
        'X-Parse-App-Build-Version':'153',
        'X-Parse-App-Display-Version':'2.22.1',
                }
#     body = '{"genre":{"variant":0,"genreUID":"Romance"},"includeStoryKeyPaths":["author"]}'
#     r = requests.post('https://production.hooked.media/parse/functions/retrieveUnreadStories',data=body,headers=headers)
#     
#     print r.content

    s  = u'000🤣00'
    print unicode(s)
    for c in s: 
        print c.encode('unicode_escape')
    print delEmoji(s)
    pass

