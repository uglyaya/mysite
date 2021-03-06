# -*- coding: UTF-8 -*-
'''
Created on 2017年4月14日
从着迷app导入数据
@author: zhouc
'''
from mysite import settings
import django,urllib2,json,urllib ,sys
django.setup() 
from hooked_server.models import BookGenre,BookAuthor,Book, BookEpisode,\
    BookDetail

print sys.path
from utils import *
            
            
def importGenre():
    BookGenre.objects.all().delete() 
    genrelist = [
        ['aiqing','爱情'],
        ['qingchun','青春'],
        ['kongbu','恐怖'], 
        ['shenmi','神秘'],
        ['jingsong','惊悚'],
        ['shaonao','烧脑'],
        ['fanzui','犯罪'],
        ['kehuan','科幻'],
        ['gaoxiao','搞笑'],
        ['huanxiang','幻想'],
        ['xuanyi','悬疑']
        ] 
    i = 1
    for genre in genrelist:
        g = BookGenre(name=genre[1],code=genre[0],seq=i)
        g.save()
        i+=1
        print genre
    print 'import book genre ok'
    

def importBook():
#     BookAuthor.objects.all().defer()
#     Book.objects.all().delete()
#     BookEpisode.objects.all().delete()
#     BookDetail.objects.all().delete()
    s = doget('http://i.zhaomistory.com/recommend/index.json?count=20000&offset=0')
    j = json.loads(s)
    for story in j['data']['storys']:
        print story['owner_nickname']
        urllib.urlretrieve(story['cover_url'], settings.MEDIA_ROOT+ '/photos/'+str(story['id'])+'.jpg')
        pic = '/photos/'+str(story['id'])+'.jpg'
        author,created = BookAuthor.objects.get_or_create(name = story['owner_nickname'])
        book,bc = Book.objects.get_or_create(
            name=story['name'],
            author = author,
            genre = BookGenre.objects.get(name=story['genre_name']),
            commentCount =100,
            summary = story['summary'],
            coverImageFile = pic,
                        ) 
        s2 = doget('http://i.zhaomistory.com/story/valid/scenes/'+str(story['id'])+'.json')
        jscene = json.loads(s2)
        seq = 1
        for id in sorted(jscene['data']['valid_scene_ids']) :
            print id
            episode,c = BookEpisode.objects.get_or_create(name='第%s章节'%seq,book=book,seq=seq) 
            s3 = doget('http://i.zhaomistory.com/story/scene/dialogs/sync/'+str(story['id'])+'/'+str(id)+'/0.json')
            jdetail = json.loads(s3)
            while True:
                for detail in jdetail['data']['dialogs']:
                    BookDetail.objects.get_or_create(sender = detail['role_name'],text=detail['publish_content'],seq=detail['id'],episode=episode,book=book)
                    print detail['id']
                if not jdetail['data']['has_more']:
                    break
                s3 = doget('http://i.zhaomistory.com/story/scene/dialogs/sync/'+str(story['id'])+'/'+str(id)+'/'+str(jdetail['data']['next_tick'])+'.json')
                jdetail = json.loads(s3)
            seq +=1
         
        
if __name__ == '__main__':
    importGenre()
    importBook()
    s2 = doget('http://i.zhaomistory.com/story/valid/scenes/7.json')
    jscene = json.loads(s2)
    print jscene['data']['valid_scene_ids']
    for id in sorted(jscene['data']['valid_scene_ids']) :
        print id
    pass