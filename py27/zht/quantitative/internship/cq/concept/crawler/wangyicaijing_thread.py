# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 22:55:36 2016

@author: Administrator
"""

import urllib2
import re
import os
from BeautifulSoup import BeautifulSoup 
import time
from selenium import webdriver
import threading


def get_href():
    url='http://quotes.money.163.com/old/#query=gn002000&DataType=HS_RANK&sort=PERCENT&order=desc&count=24&page=0'
    href=[]
    name=[]
    content=urllib2.urlopen(url).read()
    soup=BeautifulSoup(content)
    id_p=re.compile('f0-f4-f\d')
    a=soup.findAll('li',id=id_p)
    for i in range(len(a)):
        qid=re.findall('\d\d\d\d\d\d',str(a[i]))[0]
        href.append('http://quotes.money.163.com/old/#query=gn'+qid+'&DataType=HS_RANK&sort=PERCENT&order=desc&count=24&page=0')
        name.append(a[i]('a')[0].string)
        print name[-1],href[-1]
    return name,href

def get_sid(url):
    driver=webdriver.PhantomJS()
    driver.get(url)
    sid=[]
    wait=1
    while wait:
        time.sleep(0.01)
        content=driver.page_source.encode('gbk','ignore')
        soup=BeautifulSoup(content)
        for tag in soup.findAll('a',text=re.compile('\d\d\d\d\d\d')):
            if len(tag.string)==6 and (tag.string[0]=='0' or tag.string[0]=='3' or tag.string[0]=='6'):
                driver.quit()
                sid.append(tag.string)
                print tag.string
                wait=0
    return sid

def spider():
    date=time.strftime("%Y%m%d",time.localtime(time.time()))
    folder=r'c:\garbage\wangyicaijing\%s'%date
    if not os.path.isdir(folder):
        os.makedirs(folder)
        
    name,href=get_href()
    for i in range(len(href)):
        f=open(os.path.join(folder,'%d_'%i+name[i]+'.txt'),'w')
        sid=get_sid(href[i])
        for j in range(len(sid)):
            f.write(sid[j]+'\n')
        f.close()
        print i,name[i],'finished' 


date=time.strftime("%Y%m%d",time.localtime(time.time()))
folder=r'c:\garbage\wangyicaijing\threading_%s'%date
if not os.path.isdir(folder):
    os.makedirs(folder)
    
def get_data(url,name):
    print name,'work thread is started at %s'%threading.current_thread()
    global folder
    f=open(os.path.join(folder,name+'.txt'),'w')
    sid=get_sid(url)
    for j in range(len(sid)):
        f.write(sid[j]+'\n')
    f.close()
    print name,'finished','work thread is finished at %s'%threading.current_thread()


if __name__=='__main__':
    start=time.time()
    name,href=get_href()
    count=len(name)
    for i in range(count):
        threading.Thread(target=get_data,args=[href[i],name[i]]).start()
    print time.time()-start

        
    

