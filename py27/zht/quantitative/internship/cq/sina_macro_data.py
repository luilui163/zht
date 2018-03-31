# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 10:56:47 2016

@author: Administrator
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 10:39:30 2016

@author: Haitao
"""

import urllib
import urllib2
from bs4 import BeautifulSoup
import datetime
import os
import time

url='http://finance.sina.com.cn/mac/'
request=urllib2.Request(url)
response=urllib2.urlopen(request)
html=response.read().decode('gb2312')
f=open('sinahtml.txt','w')
f.write(html.encode('gb2312'))
soup=BeautifulSoup(html)
general=soup.findAll('dt',{'param':True})
generalName=['']*len(general)
for i in range(len(general)):
   # print general[i].string
    generalName[i]=general[i].string
for i in range(len(general)):
    dd=['']*len(general)
    dd[i]=general[i].parent.findAll('dd')
    #for j in range(len(dd[i])):
    #    print dd[i][j].string

cateName=['nation','price','resident','fixed','boom','foreign','fininfo','finance','industry']

today=datetime.datetime.now()
date=today.strftime('%Y%m%d')
#创建目录
if os.path.isdir(r'/home/hzhang/sina_macro_data/%s'%date):
    pass
else:
    os.makedirs(r'/home/hzhang/sina_macro_data/%s'%date)

for i in range(len(general)):
    if os.path.isdir(r'/home/hzhang/sina_macro_data/%s/%s'%(date,generalName[i])):
        pass
    else:
        os.makedirs(r'/home/hzhang/sina_macro_data/%s/%s'%(date,generalName[i]))
    dd=['']*len(general)
    dd[i]=general[i].parent.findAll('dd')
    for j in range(len(dd[i])):
        #注url中from表示起始，num表示数据个数
        url=r'http://money.finance.sina.com.cn/mac/view/vMacExcle.php?cate='+cateName[i]+'&event='+str(j)+'&from=0&num=10000&condition='
        local=r'/home/hzhang/sina_macro_data/%s/%s/%s.csv'%(date,generalName[i],dd[i][j].string)
        urllib.urlretrieve(url,local)
        time.sleep(5)

