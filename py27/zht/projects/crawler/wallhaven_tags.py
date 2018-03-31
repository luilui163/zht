# -*- coding: utf-8 -*-
"""
Created on Sat May 21 14:10:19 2016

@author: Administrator
"""

import urllib2
from bs4 import BeautifulSoup
import os
import re
from selenium import webdriver

url='https://alpha.wallhaven.cc/tags/5'
#headers={'accept-encoding':'gzip, deflate, sdch',
#         'accept-language':'zh-CN,zh;q=0.8',
#         'cache-control':'max-age=0',
#        'Referer':'https://whvn.cc/search?q=%22landscape%22&page=1',
#         'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'}

headers={'Host':'alpha.wallhaven.cc',
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'en-US,en;q=0.5',
        'Cookies':'__cfduid=de0275ca06e7c2db101b2b62e099da7691463815571; wallhaven_session=eyJpdiI6ImdUTldlS05meWpBd3VhXC9cL3pQcjgzMDZ3clQ3SVRMSzJIYStMajhzdUVjWT0iLCJ2YWx1ZSI6IlZwb3RVVWxyOUpyWmZwUTBXbGExQ3BXUXFOeVNYTmEwblZCWXhUQ2RvRE52d0cwaFZYblFRZGtHUnhwUERqSHp6eTBUTzNFNkJpWEZyUUp2eEQ5WFN3PT0iLCJtYWMiOiIxOWM1YjY2OThmMjk2MWU5YjQyY2ViNTNhNzQzM2Y4MmM4NTNkODFlNjI1Y2FjMGY4YTUyNzY5OWE4MWZiNzVlIn0%3D',
        'Accept-Encoding':"gzip, deflate, br",
        'Referer':'https://alpha.wallhaven.cc/tags/6'
        }

driver=webdriver.PhantomJS()
driver.get(url)
content=driver.page_source.encode('gbk','ignore')
driver.quit()
#req=urllib2.Request(url,headers=headers)
#content=urllib2.urlopen(req).read()
#soup=BeautifulSoup(content)







