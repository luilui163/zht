# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 16:37:59 2016

@author: hp
"""

import urllib2
import json
import threading

def one_page(page):
    url=r'http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do?&jsonCallBack=jsonpCallback62474&productId=&reportType2=DQGG&reportType=ALL&beginDate=&endDate=&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=%d&pageHelp.beginPage=%d&pageHelp.cacheSize=1&pageHelp.endPage=%d1&_=1469089651088'%(page,page,page)
#    url=r'http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do?&jsonCallBack=jsonpCallback39689&productId=&reportType2=DQGG&reportType=ALL&beginDate=&endDate=&pageHelp.pageSize=25&pageHelp.pageCount=50&pageHelp.pageNo=3205&pageHelp.beginPage=3205&pageHelp.cacheSize=1&pageHelp.endPage=32051&_=1469179004334'%()
    referer='http://www.sse.com.cn/disclosure/listedinfo/regular/'
    header={'referer':referer}
    req=urllib2.Request(url,headers=header)
    content=urllib2.urlopen(req).read()
    d=content.split('(')[1][:-1]
    js=json.loads(d)
    data=js['pageHelp']['data']
    f=open(r'C:\garbage\bullet\%d.txt'%page,'w')
    for d in data:
        f.write('%s|%s|'%(d['SSEDate'],d['security_Code']))
        f.write('%s\n'%d['title'].encode('gbk'))
    #    f.write('%s|%s|%s\n'%(d['SSEDate'],d['security_Code'],d['title'].encode('gbk')))
    f.close()
    print page
    
pages=range(1,3206)

class Consumer(threading.Thread):
    def run(self):
        global pages
        while len(pages)>0:
            page=pages.pop()
            one_page(page)

if __name__=='__main__':
    for i in range(100):
        Consumer().start()