# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 22:54:07 2016

@author: Administrator
"""
import urllib2
import re
import os
from bs4 import BeautifulSoup 
import time
import re

def get_href():
    url='http://q.10jqka.com.cn/stock/gn/'
    content=urllib2.urlopen(url).read()
    soup=BeautifulSoup(content)
    div=soup.find_all('div','cate_items')
    category=[]
    href=[]
    for i in range(0,len(div)):
        for j in range(len(div[i]('a'))):
            category.append(div[i]('a')[j].string)
            href.append(div[i]('a')[j]['href'])
            print i,j,div[i]('a')[j].string,div[i]('a')[j]['href']
    return category,href

name,href=get_href()

url=href[0]

content=urllib2.urlopen(url).read()

soup=BeautifulSoup(content)
soup_a=soup.find_all('a',href=re.compile(r'http://stockpage.10jqka.com.cn/\d\d\d\d\d\d/'),target='_blank',text=re.compile('\d\d\d\d\d\d'))
sid1=[a.string for a in soup_a if len(a.string)==6]


#test=urllib2.urlopen('http://q.10jqka.com.cn/interface/stock/detail/zdf/desc/2/3/albbgn')
#import json
#j=json.load(test)
#data=j['data']
#sid2=[d['stockcode'] for d in data]