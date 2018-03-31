#-*-coding: utf-8 -*-
#@author:tyhj

import requests
import time
import re
import pandas as pd
import random
from datetime import datetime

from bs4 import BeautifulSoup

session=requests.Session()

url1=r'http://www2.resset.cn/product/UserLogin?loginName=ctu&loginPwd=ctu123'
header1={
    'Host':'www2.resset.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Connection':'keep-alive'
}
r1=session.get(url1,headers=header1)

def getUrls():
    url2=r'http://www2.resset.cn/product/common/menu.jsp?dbMsgId=4028818a2206ecbc012206edd0d10001'
    header2={
        'Host': 'www2.resset.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Referer':'http://www2.resset.cn/product/common/mainFrame.jsp?dbMsgId=4028818a2206ecbc012206edd0d10001'
    }
    r2=session.get(url2,headers=header2)
    p="menu.add(.*);"

    items=re.findall(p,r2.content)
    parents=[]
    children=[]
    for item in items:
        t=eval(item)
        if len(t)==3:
            parents.append(t)
        elif len(t)==6:
            if len(t[3])==0:
                parents.append(t[:3])
            else:
                children.append(t[:4])

    dfP=pd.DataFrame(parents,columns=['id','parentId','name'])
    dfC=pd.DataFrame(children,columns=['id','parentId','name','url'])

    dfP=dfP.drop(dfP[dfP['parentId']==-1].index)
    dfC=dfC.drop(dfC[dfC['url']=='logout.jsp'].index)


    dfP.to_csv(r'e:\aa\dfP.csv')
    dfC.to_csv(r'e:\aa\dfC.csv')


dfC=pd.read_csv(r'e:\aa\dfC.csv',index_col=0)

tableUrls=[r'http://www2.resset.cn/product'+url[2:] for url in dfC['url']]

# tableUrl=tableUrls[0]

tableUrl3=tableUrls[10]
header3={
    'Host':'www2.resset.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
}

r3=session.get(tableUrl3,headers=header3)
soup3=BeautifulSoup(r3.content,'html')
inputs=soup3.findAll('input',{'type':'hidden'})



url4=r'http://www2.resset.cn/product/db/download/dataSearch.action'
header4={
    'Host':'www2.resset.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':tableUrl3,
    'Connection':'keep-alive'
}

def constructPayload():
    beginDate='1990-01-01'
    endDate=datetime.today().strftime('%Y-%m-%d') #TODO: change the data
    payload={}
    for p in inputs:
        if 'name' in p.attrs.keys():
            payload[p['name']]=p['value']
        if 'id' in p.attrs.keys():
            payload[p['id'][5:]]=p['value']
    payload['dateObject']='DList_Date'
    payload['beginDate']=beginDate
    payload['endDate']=endDate
    payload['cgRadio']='cg'
    payload['cSearchVar']='Stkcd'
    payload['outputType']='excel'
    payload['downType']='Column Labels+Column Names'
    payload['assignLines']='60000'

    # payload['cSearchFile']=(None,'application/octet-stream')

    return payload

payload=constructPayload()
r4=session.post(url4,headers=header4,files=payload)

print r4.content





