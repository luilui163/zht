# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 22:03:25 2016

@author: Administrator
"""

from selenium import webdriver
import re
from bs4 import BeautifulSoup
import time

url='http://q.10jqka.com.cn/stock/gn/albbgn/'
driver=webdriver.PhantomJS()
driver.get(url)
html_1=driver.page_source.encode('gbk','ignore')
sid=get_sid(html_1)

page_count=1
while True:
    try:
        next_page=driver.find_element_by_link_text('下一页')
        next_page.click()
        time.sleep(0.5)
        html=driver.page_source.encode('gbk','ignore')
        sid.append(get_sid(html))
        page_count+=1
    except:
        print page_count,'finished'
        break

#next_page.click()
#time.sleep(0.5)
#html=driver.page_source.encode('gbk','ignore')
#driver.quit()
#
#sid.append()
#print sid2

def get_sid(html):
    soup=BeautifulSoup(html)
    soup_a=soup.find_all('a',href=re.compile(r'http://stockpage.10jqka.com.cn/\d\d\d\d\d\d/'),target='_blank',text=re.compile('\d\d\d\d\d\d'))
    sid=[a.string for a in soup_a if len(a.string)==6]
    return sid
    