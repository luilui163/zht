# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 14:27:07 2016

@author: hp
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import cookielib
import re
import time
from PIL import Image
from bs4 import BeautifulSoup
import csv

'''
http://mydorm.whu.edu.cn/appdeskWeb/login?goto=http%3A%2F%2Fmydorm.whu.edu.cn%3A80%2Fihome%2Findex%3Fnull
'''


def login(username,password):
    session=requests.session()
    headers= {
            'Host':'mydorm.whu.edu.cn',
            'Referer':'http://mydorm.whu.edu.cn/appdeskWeb/login?goto=http%3A%2F%2Fmydorm.whu.edu.cn%3A80%2Fihome%2Findex%3Fnull',
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'
            }
    session.cookies = cookielib.LWPCookieJar()
    
    
    post_url = 'http://mydorm.whu.edu.cn/appdeskWeb/login?goto=http%3A%2F%2Fmydorm.whu.edu.cn%3A80%2Fihome%2Findex%3Fnull'
    postdata = {
                'goto':'http://mydorm.whu.edu.cn:80/ihome/index?null',
                'errorMessage':'',
                'username':username,
                'password':password,
                'mySubmit':'登录',
                }
    
    session.post(post_url, data=postdata, headers=headers)
    #print response1.ok
    #content1=response1.content
    #print content1
    #f=open(r'c:\garbage\login.html','w')
    #f.write(content1)
    #f.close()
    
    url='http://mydorm.whu.edu.cn/ihome/authen?decodedCookieValue=bada6e69ba4906249a4eff48c4be4733&callbackUrl=http://mydorm.whu.edu.cn:80%2Fihome%2Findex%3Fnull'
    headers={
            'Host':'mydorm.whu.edu.cn',
            'Referer':'http://mydorm.whu.edu.cn/ihome/getCookie',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
            }
    response2=session.get(url,headers=headers)
    content2=response2.content
    print content2
    f=open(r'c:\garbage\login.html','w')
    f.write(content2)
    f.close()
    pos=content2.find('我的动态')
    if pos>-1:
        print username,password
    else:
        print 'wrong'





