# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 11:14:23 2016

@author: Administrator
"""

import urllib2
import re
import os
from BeautifulSoup import BeautifulSoup 
import time


def get_href_of_one_page(url):
    
#    url='http://quote.stockstar.com/stock/blockrank_5_1_1_1.html'
    content=urllib2.urlopen(url).read()
    soup=BeautifulSoup(content)
    tbody=str(soup.findAll('tbody',id='datalist'))
    soup_tbody=BeautifulSoup(tbody)
    category=[]
    href=[]
    for i in range(len(soup_tbody('a'))):
        category.append(soup_tbody('a')[i].string.encode('gbk'))
        href.append(soup_tbody('a')[i]['href'])
    return category,href


def get_all_category_and_href():
    category,href=get_href_of_one_page(url='http://quote.stockstar.com/stock/blockrank_5_1_1_1.html')
    i=1
    while True:
        i+=1
        url='http://quote.stockstar.com/stock/blockrank_5_1_1_%d.html'%i
        content=urllib2.urlopen(url).read()
        soup=BeautifulSoup(content)
        tbody=str(soup.findAll('tbody',id='datalist'))
        if len(tbody)==32:
            break
        else:
            c,h=get_href_of_one_page(url)
            category.extend(c)
            href.extend(h)
            print i,c,h
    adjusted_href=['http://quote.stockstar.com'+hr for hr in href]
    return category,adjusted_href



def get_sid(url):
    content=urllib2.urlopen(url).read()
    soup=BeautifulSoup(content)
    tbody=str(soup.findAll('tbody',id='datalist'))
    soup_tbody=BeautifulSoup(tbody)
    sid=[]
    for i in range(0,len(soup_tbody('a')),2):
        sid.append(soup_tbody('a')[i].string)
    return sid
    
def spider():
    category,href=get_all_category_and_href()
    date=time.strftime("%Y%m%d",time.localtime(time.time()))
    folder=r'/home/hzhang/concept_test/zhengquanzhixing/%s'%date
    if not os.path.isdir(folder):
        os.makedirs(folder)

    for i in range(len(category)):
        url=href[i]
        sid=get_sid(url)
        time.sleep(2)
        f=open(os.path.join(folder,category[i]+'.txt'),'w')
        for j in range(len(sid)):
            f.write('%s\n'%sid[j])
        f.close()
        print i,category[i]


if __name__=='__main__':
    spider()


    













