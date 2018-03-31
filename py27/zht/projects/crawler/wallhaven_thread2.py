# -*- coding: utf-8 -*-
"""
Created on Fri May 20 15:48:00 2016

@author: Administrator
"""
import urllib2
import urllib
import os
import threading

count=0


folder=r'c:\garbage\pic'

urls=[]
ids=open(r'c:\garbage\wallhaven_animals.txt').read().split('\n')[:-1]
for m in ids:
    urls.append('https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-%s.jpg'%m)

headers={'accept-encoding':'gzip, deflate, sdch',
         'accept-language':'zh-CN,zh;q=0.8',
         'cache-control':'max-age=0',
        'Referer':'https://whvn.cc/search?q=%22landscape%22&page=1',
         'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}


def get_picture(url):
    global count
    req=urllib2.Request(url,headers=headers)
    try:
        content=urllib2.urlopen(req).read()
        filename=url.split('-')[1][:-4]
        f=open(r'C:\garbage\wallhaven_animals\%s.jpg'%filename, "wb")
        f.write(content)
        count+=1
        print count,filename
    except:
        pass

class Consumer(threading.Thread):
    def run(self):
        global urls
        while len(urls)>0:
            url=urls.pop()
            get_picture(url)
            
                

if __name__=='__main__':
    for i in range(200):
        Consumer().start()



