#-*-coding: utf-8 -*-
#@author:tyhj

import urllib2
from bs4 import BeautifulSoup
import datetime
import re
import time
import pandas as pd



content=urllib2.urlopen(url).read()
soup=BeautifulSoup(content)
quote=soup.findAll('div',{'id':'quotesearch'})
ul=quote[0].findAll('ul')

for i in range(len(ul)):
    qid=re.findall('\d\d\d\d\d\d',str(a[i]))[0]
    qids.append(qid)

code=content.split('SYMBOL')[1:]


sid=[s for s in sid if (s[0]=='0' or s[0]=='3' or s[0]=='6')]
sid.sort()

if not os.path.isdir(path):
    os.makedirs(path)

content=urllib2.urlopen(url).read().decode('utf-8','replace')
soup=BeautifulSoup(content)
summary=soup.findAll('div',{'class':'summary'})
s=summary[0].p
if s.font.string==u'\u6240\u5c5e\u677f\u5757':
    gn=s.contents[2].strip().split(' ')
    if len(gn)!=0:
        f=open(os.path.join(path,sid+'.txt'),'w')
        f.write('\n'.join([g.encode('gbk') for g in gn]))
        f.write('\n'.join(stocks))
        f.close()


href=[]
for i in range(1,len(soup_p)):
    for j in range(len(soup_p[i]('a'))):
        href.append(soup_p[i]('a')[j]['href'])

url=href[i].replace('Detail','Stock')[:-5]+'js'
headers={'Referer':'%s'%referer}
req=urllib2.Request(url,headers=headers)
content=urllib2.urlopen(req).read()

js=json.loads(content)
data=js['pageHelp']['data']
stock_data=js['stockData']
sid=[sd[0] for sd in stock_data]
sid=sorted(sid)

soup_a=soup.find_all('a',href=re.compile(r'http://stockpage,10jqka.com.cn/\d\d\d\d\d\d/'),
                     target='_blank',text=re.compile('\d\d\d\d\d\d'))
sid1=[s.string for a in soup_a if len(a.string)==6]


time.sleep(0.1)


for cc,hh in zip(c,h):
    if cc not in category:
        category.append(cc)
        href.append(hh)


import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}
s=requests.get(url,headers=headers)
with open(fname,'wb') as f:
    f.write(s.content)

r=requests.post('http://httpbin.org/post',data={'user':'username','pass':'password'})


import urllib
urllib.urlretrieve(url,fname)


end=datetime.date(year=2015,month=12,day=17)


job_name=item.a['title'].encode('gbk','replace')
attr=soup.select('.house-primary-content')[0]
li = attr.findAll('li', {'class': re.compile('house-primary-content-li.*?')})
rent = li[0].div.text.replace('\r\t', '').replace('\r\n', '').replace('\t', '').replace('\n', '').replace(' ', '')


stats_vote=item.find('div',{'class':'stats'}).span.i.text

content=response.text.strip()

for e,k in enumerate(pnl):
    if pd.notnull(k):
        break






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