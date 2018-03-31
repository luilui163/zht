# -*- coding: utf-8 -*-
"""
Created on Tue Aug 09 15:12:01 2016

@author: hp
"""

import requests
import cookielib
import time

def get_proxy(page):
    session=requests.session()
    session.cookies = cookielib.LWPCookieJar()
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
        }
    proxies=[]
    for page in range(1,page+1):
        url='http://www.66ip.cn/getzh.php?getzh=2016080914837&getnum=%D7%D4%BC%BA%CC%EE%D0%B4&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area='+str(page)+'&proxytype=0&api=https'
        response=session.get(url, headers=headers)
        content=response.text.strip()
        items=content.split('<br>')[:-1]
        items=[item.strip() for item in items]
        proxies+=items
        print page
    
    filename=str(int(time.time()))
    with open(r'e:\proxy\%s.txt'%filename,'w') as f:
        for proxy in proxies:
            f.write(proxy+'\n')

if __name__=='__main__':
    get_proxy(150)







