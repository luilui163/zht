# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 10:34:16 2016

@author: 13163
"""

import re
from bs4 import BeautifulSoup
import urllib2
import os
import time

def get_href():
    url='http://quotes.money.163.com/old/#query=gn002000&DataType=HS_RANK&sort=PERCENT&order=desc&count=24&page=0'
#    hrefs=[]
    names=[]
    qids=[]
    content=urllib2.urlopen(url).read()
    soup=BeautifulSoup(content)
    id_p=re.compile('f0-f4-f\d')
    a=soup.findAll('li',id=id_p)
    for i in range(len(a)):
        qid=re.findall('\d\d\d\d\d\d',str(a[i]))[0]
        qids.append(qid)
#        href.append('http://quotes.money.163.com/old/#query=gn'+qid+'&DataType=HS_RANK&sort=PERCENT&order=desc&count=24&page=0')
        names.append(a[i]('a')[0].string)
        print names[-1],qids[-1]
    return names,qids

def get_data():
    date=time.strftime("%Y%m%d",time.localtime(time.time()))
    path=r'/home/hzhang/eastmoney/%s'%date
    if not os.path.isdir(path):
        os.makedirs(path)
    names,qids=get_href()
    for q in range(len(qids)):
        page=0
        stocks=[]
        while True:
            url='http://quotes.money.163.com/hs/service/marketradar_ajax.php?host=http://quotes.money.163.com/hs/service/marketradar_ajax.php&page=%d&query=PLATE_IDS:gn%s&types=&count=28&type=query&order=desc'%(page,qids[q])
            content=urllib2.urlopen(url).read().decode('utf-8','replace')
            #content=urllib2.urlopen(url).read()
            code=content.split('SYMBOL')[1:]
            code=[c.split('NAME')[0] for c in code]
            sid=[c[3:-3] for c in code]
            page+=1
            if sid!=[]:
                for s in sid:
                    stocks.append(s)
            else:
                break
        f=open(os.path.join(path,names[q]+'.txt'),'w')
        f.write('\n'.join(stocks))
        f.close()
        print qids[q],names[q]
    
if __name__=='__main__':
    get_data()