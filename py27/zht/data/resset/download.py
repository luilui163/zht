#-*-coding: utf-8 -*-
#@author:tyhj
import requests
from bs4 import BeautifulSoup
import pandas as pd


url=r'http://www2.resset.cn/product/upload/dataDictionary/CN/THRFACDAT_MONTHLY.htm'
r=requests.get(url)

soup=BeautifulSoup(r.content,'html')

form=soup.find('form')
title=form.span.text
trs=form.find_all('tr',{'class':'tableShow'})

data=[[td.text for td in tr] for tr in trs]
df=pd.DataFrame(data)
df.to_excel('test.xls',encoding='utf8')



url2=r'http://www2.resset.cn/product/common/main.jsp'
r2=requests.get(url2)
print r2.status_code
with open('content2.html','w') as f:
    f.write(r2.content)


