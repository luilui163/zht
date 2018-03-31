# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 06:30:04 2016

@author: Administrator
"""

import re
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import cookielib





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
            category.append(soup_p[i]('a')[j].string)
            href.append(soup_p[i]('a')[j]['href'])
#            print soup_p[i]('a')[j].string,soup_p[i]('a')[j]['href']
    
    return category,href

category,href=get_href()

#def get_sid(url):
#    content=urllib2.urlopen(url).read()
#    sid=re.findall('[036]\d\d\d\d',content)
#    return sid
#    
#url=href[0][:-5]+'js'
#content=urllib2.urlopen(url).read()
url='http://stock.jrj.com.cn/concept/conceptdetail/conceptDetail_ds7.js'

headers={
'Accept-Encoding':'gzip,deflate, sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
}

req=urllib2.Request(url,headers=headers)
html=urllib2.urlopen(req)

#cookieJar=cookielib.CookieJar()
## 实例化一个全局opener
#opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
## 获取cookie
#req=urllib2.Request(url,headers=headers)
#result = opener.open(req)
## 显示结果
#print result.read()

ckjar = cookielib.MozillaCookieJar(r'c:\garbage\cookie.txt')
ckproc = urllib2.HTTPCookieProcessor(ckjar)
opener = urllib2.build_opener(ckproc)
f = opener.open(req) 
htm = f.read() 
f.close()


cookiejar=cookielib.CookieJar()
handler=urllib2.HTTPCookieProcessor(cookiejar=cookiejar)
opener=urllib2.build_opener(handler,urllib2.HTTPHandler(debuglevel=1))
#后边加的urllib2.HTTPHandler是为了打印出调试信息
s=opener.open(url)
print s.read(100)




#if __name__=='__main__':
#    category,href=get_href()
