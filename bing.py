# -*- coding:utf-8 -*-
import urllib2
import urllib
import cookielib
import re

class bingPicture(object):
    def __init__(self):
        self.url='http://cn.bing.com/images?FORM=Z9LH'
        self.fw=open('bing.txt','wb')
    
    def getImg(self,item):
        imgData=urllib2.urlopen(item[0]).read()
        img=open(item[1].decode('utf-8')+'.jpg','wb')
        img.write(imgData)
        img.close()
    
    def getPicture(self):
        header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
        request=urllib2.Request(self.url,headers=header)
        response=urllib2.urlopen(request)
        pattern=re.compile('ilp_.u" src="(.*?)&.*?alt="(.*?)" ', re.S)
        items=re.findall(pattern, response.read())
        for item in items:
            self.getImg(item)
        

bing=bingPicture()
bing.getPicture()