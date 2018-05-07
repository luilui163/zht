#-*-coding: utf-8 -*-
#author:tyhj
#crawler_zncj.py 2017/7/23 22:00
import requests
from bs4 import BeautifulSoup
import json
import time
import os
import pandas as pd
from pandas.io.json import json_normalize
import re

import sqlalchemy
from sqlalchemy.types import TEXT


session=requests.Session()

#======================================================================================
url2=r'http://202.114.238.112:8000/login'
header2={
    'Host':'202.114.238.112:8000',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Origin':'http://202.114.238.112:8000/login'
}
form2={
    'userId':,#
    'password':,
}


r2=session.post(url2,headers=header2,data=form2)
with open('c2.html','w') as f:
    f.write(r2.content)

#===========================================================================================
url3=r'http://202.114.238.112:8000/rwt/CSMAR/http/P75YPLUHPSRYE65DF3SX85B/Home'
header3={
    'Host':'202.114.238.112:8000',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
}
r3=session.get(url3,headers=header3)
soup=BeautifulSoup(r3.content,'html')
a=soup.find('input',{'type':'hidden','id':'hdUser'})
value=a['value']

#========================================================================
#jump to new system,and r4 is necessary for the process following
url4 = r'http://cn.gtadata.com//Base/ChangeLanguage?lang=Zh_cn&returnUrl=%s&s=Home/Index' % value
header4 = {
    'Host': 'cn.gtadata.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer': 'http://202.114.238.112:8000/rwt/CSMAR/http/P75YPLUHPSRYE65DF3SX85B/Home'
}

r4 = session.get(url4, headers=header4)


#===============================================================

url5=r'http://cn.gtadata.com/SingleTable'
header5={
    'Host':'cn.gtadata.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://cn.gtadata.com/Home/Index'
}

r5=session.get(url5,headers=header5)

with open('c5.html','w') as f:
    f.write(r5.content)


soup5=BeautifulSoup(r5.content)

series=soup5.findAll('li',{'seriesid':True})
seriesItems=[]
for s in series:
    seriesItems.append((s['seriesid'],s.text))

databases=[]
for si in seriesItems:
    url6=r'http://cn.gtadata.com/SingleTable/GetDataBase?seriesid=%s'%si[0]
    header6=header5
    r6=session.get(url6,headers=header6)

    soup6=BeautifulSoup(r6.content)
    aas=soup6.findAll('a',{'href':True,'target':'_parent'})
    for a in aas:
        href=a['href']
        dbid=a['dbid']
        dbname=a.text
        databases.append((si[0],si[1],href,dbid,dbname))
    print si

# databaseDF=pd.DataFrame(databases,columns=['seriesid','seriesname','href','dbid','dbname'])
# databaseDF.to_csv(r'D:\quantDb\sourceData\gta\data\databases.csv',encoding='gbk')

#=============================================================================================
#download reference pdfs
# for i,item in enumerate(databases):
#     dbid=item[3]
#     url=r'http://cn.gtadata.com/SingleTable/UseHelper?dbid=%s'%dbid
#     # url=r'http://cn.gtadata.com/SingleTable/DBInstructions'
#     header=header5
#     form={'id':dbid}
#     r=session.get(url,headers=header)
#
#     with open('pdf.pdf','wb') as f:
#         f.write(r.content)


tickers=[]
count=0
for i,item in enumerate(databases):
    seriesid=item[0]
    seriesname=item[1]

    url5='http://cn.gtadata.com'+item[2][2:]
    dbid=item[3]
    dbname=item[4]

    header5={
        'Host':'cn.gtadata.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Referer':'http://cn.gtadata.com/Home'
    }

    r5=session.get(url5,headers=header5)
    soup=BeautifulSoup(r5.content)
    lis=soup.findAll('li',{'nodename':True,'codetype':True,'nodeid':True,'tbid':True})


    # tableItems=[[item[0],item[1],item[2],li['nodename'],li['nodeid'],li['tbid']] for li in lis]

    tableItems=[[seriesid,seriesname,url5,dbid,dbname,li['nodename'],li['nodeid'],li['tbid']] for li in lis]

    tickers+=tableItems

    for j,tableItem in enumerate(tableItems):
        url6 = r'http://cn.gtadata.com/SingleTable/TreeNodeSelected?treeNodeId=%s&projectId=null&tbId=%s' % (tableItem[6], tableItem[-1])
        header6={
            'Host':'cn.gtadata.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Referer':'http://cn.gtadata.com/SingleTable/DataBaseInfo?nodeid=110'
        }

        form6={
            'treeNodeId':tableItem[6],
            'projectId':'null',
            'tbId':tableItem[-1]
        }
        r6=session.post(url6,data=form6,headers=header6)
        dic=json.loads(r6.content)
        with open(r'D:\quantDb\sourceData\gta\data\json\%s_%s.txt'%(tableItem[-2],tableItem[-1]),'w') as f:
            json.dump(dic,f)
        print count,i,j,tableItem[0],tableItem[3]
        count+=1
df=pd.DataFrame(tickers)
df.columns=['seriesid','seriesname','url','dbid','dbname','nodename','nodeid','tbId']
df.to_csv(r'D:\quantDb\sourceData\gta\data\tickers1.csv',encoding='gbk')


