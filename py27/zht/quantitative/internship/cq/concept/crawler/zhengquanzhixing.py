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
        c,h=get_href_of_one_page(url)
        if c==[]:
            break
        else:
            for cc,hh in zip(c,h):
                if cc not in category:
                    category.append(cc)
                    href.append(hh)
        print i
#注意下一页的第一支股票与上一页的最后一只股票是相同的
    adjusted_href=['http://quote.stockstar.com'+hr for hr in href]
    return category,adjusted_href

def get_sid(url):
    while True:
        try:
            content=urllib2.urlopen(url).read()
            soup=BeautifulSoup(content)
            tbody=str(soup.findAll('tbody',id='datalist'))
            soup_tbody=BeautifulSoup(tbody)
            sid=[]
            for i in range(0,len(soup_tbody('a')),2):
                sid.append(soup_tbody('a')[i].string)
            return sid
            break
        except Exception as inst:
            print inst
            time.sleep(2)


def collect_sids(url):
    sids=[]
    i=1
    while True:
        url='_'.join(url.split('_')[:-1])+'_'+str(i)+'.html'
#        url=url[:-6]+str(i)+'.html'
    #    url=r'http://quote.stockstar.com/stock/blockperformance_5_400124989_2_1_%d.html'%i
        tmp=get_sid(url)
        if tmp==[]:
            break
        sids+=[t for t in tmp if t not in sids]
        i+=1
#        print i 
    sids=sorted(sids)
    return sids

def spider():
    category,href=get_all_category_and_href()
    date=time.strftime("%Y%m%d",time.localtime(time.time()))
    folder=r'/dat/datadev/workspace/concept/zhengquanzhixing/%s'%date
    if not os.path.isdir(folder):
        os.makedirs(folder)
    for i in range(len(category)):
        url=href[i]
        sids=collect_sids(url)
        f=open(os.path.join(folder,category[i]+'.txt'),'w')
        f.write('\n'.join(sids))
        f.close()
        print i,category[i]


if __name__=='__main__':
    spider()


    













