# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 12:46:40 2016

@author: hp
"""

import urllib2
from bs4 import BeautifulSoup
import re
import csv

def get_provinces():
    url='http://u.feelingmsg.com/u/'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
    req=urllib2.Request(url,headers=headers)
    content=urllib2.urlopen(req).read()
    soup=BeautifulSoup(content)
    p=re.compile('.*?.php')
    items=soup.find_all('a',{'target':'blank','href':p})
    provinces=[]
    for item in items:
        href='http://u.feelingmsg.com/u/'+item['href']
        prov=item.string.encode('gbk','replace')
        provinces.append((href,prov))
    return provinces
    
def get_info(province):
    url=province[0]
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
    req=urllib2.Request(url,headers=headers)
    content=urllib2.urlopen(req).read()
    soup=BeautifulSoup(content)
    items=soup.find_all('a',{'href':True,'target':'_blank'})
    info=[]
    for item in items[2:-2]:
        try:
            href=item['href']
            name=item.string.encode('gbk','replace')
            info.append((name,province[1],href))
        except:
            pass
    print province[1]
    return info


def save_data():
    provinces=get_provinces()
    info=[]
    for province in provinces:
        info+=get_info(province)
    csvfile = file(r'c:\garbage\university_info.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(['name','province','href'])
    writer.writerows(info)
    csvfile.close()
    
if __name__=='__main__':
    save_data()
    



