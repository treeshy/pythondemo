# -*- coding:utf-8 -*-
import urllib2
import urllib
import cookielib
import re
 
 
class qsbk(object):
    def __init__(self):
        self.pageIndex=0
        self.baseUrl='http://www.qiushibaike.com/8hr/page/'
        self.header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
        self.enable=False
        self.stories=[]
        self.fw=open('qiushibaike.txt','wb')
     
    def getPage(self):
        try:
            url=self.baseUrl+str(self.pageIndex)
            request=urllib2.Request(url,headers=self.header)
            response=urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError,e:
            if hasattr(e, 'reason'):
                print '�������°ٿ�ʧ�ܣ�����ԭ��',e.reason
                return None
 
    def getPageItems(self):
        content=self.getPage()
        if not content:
            print '����ҳ��ʧ��...'
            return None
        pattern=re.compile('h2>(.*?)<.*?content">(.*?)</div.*?number">(.*?)</.*?number">(.*?)</', re.S)
        items=re.findall(pattern, content)
        for item in items:
            pageStories=[]
            for i in item:
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR,"\n",i)
                self.fw.write(text+'\r\n')
                pageStories.append(text)
            self.fw.write('\r\n')
            self.stories.append(pageStories)
        
    def getOneStory(self):
        input=raw_input()
        if input=='Q':
            self.fw.close()
            self.enable=False
            return
        if len(self.stories)<1:
            self.getPageItems()
            self.pageIndex+=1
        pageStories=self.stories[0]
        print '��%dҳ\t�����ˣ�%s\t�������ݣ�%s\t��������%s\t��������%s'%(self.pageIndex,pageStories[0],pageStories[1],
                                                       pageStories[2],pageStories[3])
        del self.stories[0]
          
    def start(self):
        print u'���ڶ�ȡ���°ٿƣ��س��鿴�¶��ӣ�Q���˳�'
        self.enable=True
        while self.enable:
            self.getOneStory()

spider=qsbk()
spider.start()