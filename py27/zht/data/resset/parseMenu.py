#-*-coding: utf-8 -*-
#@author:tyhj

from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os

def parseMenu():
    content=open('menu1.txt').read()

    p=r'menu.add(.*);'
    parents=[]
    chs=[]
    items=re.findall(p,content)
    for item in items:
        item=item.replace('menu.add(','')
        item=item.replace(');','')
        if len(item.split(','))==3:
            a,b,c=item.split(',')
            parents.append([a[2:-1],b[1:-1],c[1:-2]])
        elif len(item.split(','))==6:
            id=item.split(',')[0][2:-1]
            parent=item.split(',')[1][1:-1]
            name=item.split(',')[2][1:-1]
            tableName=item.split(',')[3].split('=')[2][:-8]
            chs.append([id,parent,name,tableName])

    dfP=pd.DataFrame(parents)
    dfC=pd.DataFrame(chs)

    dfP.to_csv('dfP.csv')
    dfC.to_csv('dfC.csv')

def getAllDoc():
    dfC=pd.read_csv(r'dfC.csv',index_col=0)
    names=dfC['3']
    for name in names:
        url=r'http://www2.resset.cn/product/upload/dataDictionary/CN/%s.htm'%name
        r=requests.get(url)
        with open(r'D:\quantDb\sourceData\resset\doc\%s.htm'%name,'w') as f:
            f.write(r.content)
        print name

def combineMenu():
    import os
    directory=r'D:\quantDb\sourceData\resset\doc'
    fns=os.listdir(directory)
    with open(r'D:\quantDb\sourceData\resset\combined.htm','w') as f:
        for fn in fns:
            f.write(open(os.path.join(directory,fn)).read())


def parseItems():
    directory=r'D:\quantDb\sourceData\resset\doc'

    fns=os.listdir(directory)
    dfs=[]
    for i,fn in enumerate(fns):
        content=open(os.path.join(directory,fn)).read()
        soup=BeautifulSoup(content,'html')
        form=soup.findAll('form',attrs={'method':'post'})
        name=form.span.string
        table=form.find('table',{'class':'listTable'})
        trs=table.findAll('tr',{'class':'tableShow'})
        items=[[td.string for td in tr] for tr in trs]
        df=pd.DataFrame(items,index=[name]*len(items),columns=['variable','nameCN','nameEN','type','length','unit','comment'])
        dfs.append(df)
        print i,len(form)
    combined=pd.concat(dfs,axis=0)

    # combined.to_csv(r'D:\quantDb\sourceData\resset\combined.csv',encoding='gb18030')
    combined.to_csv(r'D:\quantDb\sourceData\resset\combined.csv',encoding='utf8')
