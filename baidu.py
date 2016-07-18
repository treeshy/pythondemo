# -*- coding:utf-8 -*-
import urllib2
import urllib
import cookielib
import re

baseUrl='http://tieba.baidu.com/p/3138733512'

class tools:
    replaceImg=re.compile('<img.*?>')
    replaceAddr=re.compile('<a.*?>|</a>')
    replaceLine=re.compile('<tr>|<div>|</div>|</p>')
    replaceTD=re.compile('<td>')
    replacePara=re.compile('<p.*?>')
    replaceBR=re.compile('<br><br>|<br>')
    repalceExtraTag=re.compile('<.*?>')
    def replace(self,txt):
        txt=re.sub(self.replaceImg,"",txt)
        txt=re.sub(self.replaceAddr,"",txt)
        txt=re.sub(self.replaceLine,'\r\n',txt)
        txt=re.sub(self.replaceTD,'\t',txt)
        txt=re.sub(self.replacePara,'\r\n  ',txt)
        txt=re.sub(self.replaceBR,'\r\n',txt)
        txt=re.sub(self.repalceExtraTag,'',txt)
        return txt.strip()
    
class bdtb(object):
    def __init__(self,baseUrl,see_lz):
        self.baseUrl=baseUrl
        self.see_lz='?see_lz='+str(see_lz)
        self.tool=tools()
        self.fw=open('baidutieba.txt','wb')
        self.floor=1
        
    def getPage(self,pageNum):
        try:
            url=self.baseUrl+self.see_lz+'&pn='+str(pageNum)
            request=urllib2.Request(url)
            response=urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError,e:
            if hasattr(e, 'reason'):
                print '���Ӱٶ����ɳ��֣�����ԭ��',e.reason
                return None
    
    def getTitle(self,page):
        pattern=re.compile('<h3.*?title=(.*?) style', re.S)
        result=re.search(pattern, page)
        if result:
            self.fw.write(result.group(1).strip()+'\r\n')
            return result.group(1).strip()
        else:
            return None
        
    def getPageNum(self,page):
        pattern=re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result=re.search(pattern, page)
        if result:
            self.fw.write(result.group(1).strip()+'\r\n')
            return result.group(1).strip()
        else:
            return None
    
    def getContent(self,page):
        pattern=re.compile('id="post_content_.*?>(.*?)</div', re.S)
        items=re.findall(pattern, page)
        for item in items:
            self.fw.write(str(self.floor))
            self.fw.write("¥------------------------------------------------------------------------------------------------------------------------------------\r\n")
            self.fw.write(self.tool.replace(item)+'\r\n')
            self.floor+=1
            
    def start(self):
        basePage=self.getPage(1)
        pageNum=self.getPageNum(basePage)
        title=self.getTitle(basePage)
        if pageNum==None:
            print '��ַʧЧ�������ԡ�'
            return
        try:
            print '�����ӹ���%sҳ'%pageNum
            for i in range(1,int(pageNum)+1):
                print '����д���%dҳ'%i
                page=self.getPage(i)
                self.getContent(page)
        except IOError,e:
            print 'д���쳣��ԭ��'+e.message
        finally:
            print 'д�����'
            
    
print '���������Ӵ��ţ�'
baseUrl='http://tieba.baidu.com/p/'+str(raw_input('http://tieba.baidu.com/p/'))
print '�Ƿ�ֻ��¥������=1����=0:'
see_lz=int(raw_input())
spider=bdtb(baseUrl,see_lz)
spider.start()