# -*- coding:utf-8 -*-
import urllib2
import urllib
import cookielib
import re
 
class jwc(object):
     
    def __init__(self,zjh,mm,type):
        self.loginUrl='http://202.115.47.141/loginAction.do'
        self.evaUrl='http://202.115.47.141/jxpgXsAction.do?oper=listWj'
        self.postdata=urllib.urlencode({
                       'zjh':zjh,
                       'mm':mm})
        self.cookies=cookielib.CookieJar()
        self.opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
        self.type=type
        self.fw=open('jwc.txt','wb')
         
    def getScore(self):
        totalElectiveCredit=0.0
        totalElectiveScore=0.0
        totalRequiredCredit=0.0
        totalRequireScore=0.0
        scoreUrl='http://202.115.47.141/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2015-2016%D1%A7%C4%EA%B4%BA(%C1%BD%D1%A7%C6%DA)'
        response=self.opener.open(scoreUrl)
        pattern=re.compile('class="odd.*?/td>.*?/td>.*?center">(.*?)</td'+
                           '.*?/td>.*?center">(.*?)</td'+
                           '.*?center">(.*?)</td'+
                           '.*?p align="center">(.*?)&nbsp', re.S)
        items=re.findall(pattern, response.read())
        
        for item in items:
            i0=item[0].strip().decode('gbk')#名称
            i1=float(item[1].strip())#学分
            i2=item[2].strip().decode('gbk')#必修|选修
            i3=0.0
            i33=item[3].strip().decode('gbk')#成绩
            self.fw.write(i0.encode('utf-8')+' '+str(i1)+' '+i2.encode('utf-8')+' '+i33.encode('utf-8')+'\r\n')
            if i33=='优秀'.decode('utf-8'):
                i3=95.0
            elif i33=='良好'.decode('utf-8'):
                i3=85.0
            elif i33=='及格'.decode('utf-8'):
                i3=75.0
            elif i33=='不及格'.decode('utf-8'):
                i3=30.0
            else:
                i3=float(i33.encode('utf-8'))
            if i2=='必修'.decode('utf-8'):
                if i1==0:
                    i1=0.25
                totalRequireScore+=i3*i1
                totalRequiredCredit+=i1
            else:
                totalElectiveScore+=i3*i1
                totalElectiveCredit+=i1
        self.fw.write('\r\n')
        if self.type==1:
            self.fw.write('所有必修总均分为：%.2f'%(totalRequireScore/totalRequiredCredit))
        else:
            self.fw.write('总均分为：%.2f'%((totalElectiveScore+totalRequireScore)/(totalElectiveCredit+totalRequiredCredit)))
        self.fw.close()
        
    def getTotalItems(self):
        response=self.opener.open(self.evaUrl)
        #self.fw.write(response.read())
        pattern=re.compile('rows=(.*?)&', re.S)
        items=re.findall(pattern, response.read().decode('gbk').encode('utf-8'))
        return items[0]
    
    def evalute(self):
        response=self.opener.open(self.evaUrl)
        itemNum=0
        totalItems=self.getTotalItems()
        evaluteUrl='http://202.115.47.141/jxpgXsAction.do?totalrows='+totalItems+'&page='
        evaluteDetailUrl='http://202.115.47.141/jxpgXsAction.do'
        
        pattern=re.compile('class="odd.*?/td>.*?/td>.*?/td>'+
                           '.*?center">(.*?)</td'+
                           '.*?name="(.*?)#@(.*?)#@(.*?)#@(.*?)#@(.*?)#@(.*?)" .*?', re.S)
        items=re.findall(pattern, response.read())
        for item in items:
                  postdata=urllib.urlencode({'wjbm':item[1],
                            'bpr':item[2],
                            'pgnr':item[6],
                            'oper':'wjResultShow',
                            'wjmc':item[4],
                            'bprm':item[3],
                            'pgnrm':item[5],
                            'pageSize':20,
                            'page':itemNum/20+1,
                            'currentPage':itemNum/20+1
                            })
                  request=urllib2.Request(evaluteUrl+str(itemNum/20+1)+'&pageSize=20',postdata)
                  res=self.opener.open(request)
                  self.fw.write(res.read())
                  #print item[0],item[1],item[2],item[3],item[4],item[5],item[6]
                  itemNum+=1
        
    def start(self):
        request=urllib2.Request(self.loginUrl,self.postdata)
        response=self.opener.open(request)
        if self.type==1|self.type==2:
            self.getScore()
        else:
            self.evalute()
        #self.fw.write(response.read())
         
 
 
#zjh=raw_input('请输入学号：')
#mm=raw_input('请输入密码：')
#type=int(raw_input('计算绩点(仅必修)输入1,计算绩点(所有)输入2,一键评教输入3：'))
zjh='2013141222065'
mm='*******'
type=3
me=jwc(zjh,mm,type)
me.start()
