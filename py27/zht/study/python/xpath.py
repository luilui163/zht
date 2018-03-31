# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 12:07:40 2016

@author: hp
"""

import urllib2 
from lxml import etree

url='http://www.dmoz.org/Computers/Programming/Languages/Python/Books'
content=urllib2.urlopen(url).read()
with open(r'c:\garbage\content.html','w') as fp:
    fp.write(content)
    
tree=etree.HTML(content)
divs=tree.xpath('//*[@id="site-list-content"]/div')
items=[]
for div in divs:
    item={}
    item['title']=div.xpath('div[3]/a/div/text()')[0]
    item['link']=div.xpath('div[3]/a/@href')[0]
    item['desc']=div.xpath('div[3]/div/text()')[0].strip()
    items.append(item)
print items[0]['desc']