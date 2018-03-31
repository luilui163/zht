# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 06:30:04 2016

@author: Administrator
"""
import re
from BeautifulSoup import BeautifulSoup
import urllib2
import time
import os
import json


def get_href():
    url='http://stock.jrj.com.cn/concept/conceptpage.shtml'
    res=urllib2.urlopen(url)
    html=res.read()
    #print html
    soup=BeautifulSoup(html)
    soup_p=soup.findAll('p','class'=='jrj-clear')
    category=[]
    href=[]
    for i in range(1,len(soup_p)):
        for j in range(len(soup_p[i]('a'))):
            category.append(soup_p[i]('a')[j].string.encode('gbk'))
            href.append(soup_p[i]('a')[j]['href'])
#            print soup_p[i]('a')[j].string,soup_p[i]('a')[j]['href']
    
    return category,href

def crawler():
    category,href=get_href()
    date=time.strftime("%Y%m%d",time.localtime(time.time()))
    folder=r'/dat/datadev/workspace/concept/jinrongjie/%s'%date
    #folder=r'c:\garbage\jinrongjie'
    if not os.path.isdir(folder):
        os.makedirs(folder)
    
    i=0
    for i in range(len(href)):
        referer=href[i]
        url=href[i].replace('Detail','Stock')[:-5]+'js'
        headers={'Referer':'%s'%referer}
        req=urllib2.Request(url,headers=headers)
        content=urllib2.urlopen(req).read()
        content=content.split('=')[1][:-1]
        js=json.loads(content)
        stock_data=js['stockData']
        sid=[sd[0] for sd in stock_data]
        sid=sorted(sid)
        f=open(os.path.join(folder,category[i])+'.txt','w')
#        sid=re.findall('[036]\d\d\d\d\d',content)
#        sid=sorted(sid)
        for j in range(len(sid)):
            f.write('%s\n'%sid[j])
        f.close()
        print i,category[i]

if __name__=='__main__':
    crawler()
