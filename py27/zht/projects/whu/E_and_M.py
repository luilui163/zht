# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 22:01:45 2016

@author: hp
"""

import urllib2
from bs4 import BeautifulSoup

def get_xwsd():
    items=[]
    for page in range(1,122):
        if page==1:
            url='http://ems.whu.edu.cn/xwsd/index.html'
        else:
            url='http://ems.whu.edu.cn/xwsd/index_{page}.html'.format(page=page)
        headers={
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'        
                }
        req=urllib2.Request(url,headers=headers)
        content=urllib2.urlopen(req).read().decode('gb2312','replace')
        #print content
        soup=BeautifulSoup(content)
        listmb=soup.find_all('div',{'class':'listmb'})[0]
        lis=listmb.find_all('li')
        for li in lis:
            date=li.span.contents[0]
            href='http://ems.whu.edu.cn/'+li.a['href']
            title=li.a.contents[0]
            items.append((date,title,href))
        print page
    return items
    
def get_tzgg():
    items=[]
    for page in range(1,103):
        if page==1:
            url='http://ems.whu.edu.cn/tzgg/index.html'
        else:
            url='http://ems.whu.edu.cn/tzgg/index_{page}.html'.format(page=page)
        headers={
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'        
                }
        req=urllib2.Request(url,headers=headers)
        content=urllib2.urlopen(req).read().decode('gb2312','replace')
        #print content
        soup=BeautifulSoup(content)
        listmb=soup.find_all('div',{'class':'listmb'})[0]
        lis=listmb.find_all('li')
        for li in lis:
            date=li.span.contents[0]
            href='http://ems.whu.edu.cn/'+li.a['href']
            title=li.a.contents[0]
            items.append((date,title,href))
        print page
    return items
    
xwsd=get_xwsd()
tzgg=get_tzgg()


