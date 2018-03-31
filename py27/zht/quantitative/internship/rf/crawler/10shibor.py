#-*-coding: utf-8 -*-
#@author:tyhj

from bs4 import BeautifulSoup
import urllib2
import time


date=time.strftime("%Y%m%d",time.localtime(time.time()))
url='http://data.eastmoney.com/shibor/default.html'
content=urllib2.urlopen(url).read().decode('gb2312')
soup=BeautifulSoup(content)
table=soup.find_all('table')[0]
items=table.find_all('tr')[1:]
filename=r'C:\rf\shibor\%s.txt'%date
with open(filename,'w') as f:
    for item in items:
        tds = item.find_all('td')
        type = tds[0].a.text.encode("gb2312")
        rate = tds[1].text
        bp = tds[2].text
        f.write('{},{},{}\n'.format(type,rate,bp))










