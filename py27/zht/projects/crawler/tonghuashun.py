# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 11:21:16 2016

@author: 13163
"""
import re
from bs4 import BeautifulSoup
import time
import urllib2

stocks=open(r'c:\cq\stock.txt').read().split('\n')[:-1]

f=open(r'c:\garbage\gn.txt','w')
count=0
for stock in stocks:
    url='http://stockpage.10jqka.com.cn/%s/'%stock[:6]
    #html=urllib2.urlopen(url).read()
    html=urllib2.urlopen(url).read().decode('utf-8','replace')
    #html=unicode(html,'utf-8','ignore').encode('gbk','ignore')
    soup=BeautifulSoup(html)
    try:
        soup_dl=soup.findAll('dl',{'class':'company_details'})[0]
        soup_gn=soup_dl.findAll(title=True)[0]
        title=soup_gn['title']
        pattern=re.compile(u'[，,]')
        gn=pattern.split(title)
        gn=[g.encode('gbk') for g in gn]
        f.write(stock+'\t'+'\t'.join(gn)+'\n')
        print count,stock
        
    except IndexError,e:
        print count,stock,e
    count+=1
#    for i in range(len(gn)):
#        print gn[i]
#        
#    for j in range(len(gn)):
#        f.write(gn[j].encode('gbk')+'\n')
f.close()











