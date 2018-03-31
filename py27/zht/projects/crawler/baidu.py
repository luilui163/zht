# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 18:26:39 2016

@author: hp
"""

import os
import urllib2
import urllib
import re



def index_href(item):
    if item.find('href = ')!=-1:
        return item.find('href = ')+7
    elif item.find('href= ')!=-1:
        return item.find('href= ')+6
    elif item.find('href =')!=-1:
        return item.find('href =')+6
    elif item.find('href=')!=-1:
        return item.find('href=')+5

def index_target(item):
    if item.find('target')!=-1:
        return item.find('target')

def get_url(wd):
    wd=urllib.urlencode({'wd':wd})
    url='http://www.baidu.com/s?'+wd
    page=urllib2.urlopen(url).read()
    content=(page.decode('utf-8')).replace('\n','').replace('\t','')
    title=re.findall(r'<div class="result.*?</h3>',content)
    title=[item[index_href(item):index_target(item)] for item in title]
    title=[item.replace(' ','').replace('"','') for item in title]
    for i,item in enumerate(title):
        print i,item

wd='python'
get_url(wd)