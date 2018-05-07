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


def getJson():
    session=requests.Session()

    #======================================================================================
    url2=r'http://202.114.238.112:8000/login'
    header2={
        'Host':'202.114.238.112:8000',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Origin':'http://202.114.238.112:8000/login'
    }
    form2={
        'userId':'z0003977',#
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

    # with open('c3.html','w') as f:
    #     f.write(r3.content)



    #==============================================================================================
    url4=r'http://cn.gtadata.com//Base/ChangeLanguage?lang=Zh_cn&returnUrl=%s&s=Home/Index'%value
    header4={
        'Host':'cn.gtadata.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Referer':'http://202.114.238.112:8000/rwt/CSMAR/http/P75YPLUHPSRYE65DF3SX85B/Home'
    }

    r4=session.get(url4,headers=header4)
    soup=BeautifulSoup(r4.content)
    dls=soup.findAll('dl',{'class':'subscriber-list'})
    items=[]
    for dl in dls:
        category=dl.dt.a.text
        for dd in dl.findAll('dd'):
            items.append([category,dd.a.string,dd.a['href']])

    with open('item.txt','w') as f:
        for item in items:
            row=('\t'.join(item)+'\n').encode('gbk')
            f.write(row)

    #=============================================================================================
    tickers=[]
    count=0
    for i,item in enumerate(items):
        url5='http://cn.gtadata.com'+item[-1][2:]
        header5={
            'Host':'cn.gtadata.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Referer':'http://cn.gtadata.com/Home'
        }

        r5=session.get(url5,headers=header5)
        soup=BeautifulSoup(r5.content)
        lis=soup.findAll('li',{'nodename':True,'codetype':True,'nodeid':True,'tbid':True})
        tableItems=[[item[0],item[1],item[2],li['nodename'],li['nodeid'],li['tbid']] for li in lis]
        tickers+=tableItems

        for j,tableItem in enumerate(tableItems):
            url6 = r'http://cn.gtadata.com/SingleTable/TreeNodeSelected?treeNodeId=%s&projectId=null&tbId=%s' % (tableItem[4], tableItem[5])
            header6={
                'Host':'cn.gtadata.com',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
                'Referer':'http://cn.gtadata.com/SingleTable/DataBaseInfo?nodeid=110'
            }

            form6={
                'treeNodeId':tableItem[4],
                'projectId':'null',
                'tbId':tableItem[5]
            }
            r6=session.post(url6,data=form6,headers=header6)
            dic=json.loads(r6.content)
            with open(r'D:\quantDb\sourceData\gta\data\json\%s_%s.txt'%(tableItem[-2],tableItem[-1]),'w') as f:
                json.dump(dic,f)
            print count,i,j,tableItem[0],tableItem[3]
            count+=1
    df=pd.DataFrame(tickers)
    df.columns=['dbname','category','url','tbname','treeNodeId','tbId']
    df.to_csv(r'D:\quantDb\sourceData\gta\data\tickers.csv',encoding='gbk')


def _filterSpecialChar(x):
    if x:
        return x.replace('\t','').replace('\n','').replace('\r','')

def parseJson():
    dirpath=r'D:\quantDb\sourceData\gta\data\json'
    fns=os.listdir(dirpath)
    tables=[]
    for i,fn in enumerate(fns):
        dic=json.loads(open(os.path.join(dirpath,fn)).read())
        print i, dic['TBName']
        table=json_normalize(dic['TableFieldViewListSet'])
        table['DBTitle']=dic['DBTitle']
        table['NoteTitle']=dic['TableView']['NodeTitle']
        table['TBTitle']=dic['TableView']['TBTitle']
        table['TBName']=dic['TBName']
        table['url']=dic['DownSimplePath']
        table['StartTime']=dic['TableView']['StartTime']
        table['EndTime']=dic['TableView']['EndTime']

        vars=['DBTitle','NoteTitle','TBTitle','TBName','Fldname','Title','Typename','Description','StartTime','EndTime','Mergerdatatype','url']
        colnames=vars+[col for col in table.columns if col not in vars]
        table=table[colnames]
        # table=table.sort_values(['DBTitle','NoteTitle','TBTitle','TBName','Fldname'])

        table['Description']=table['Description'].apply(_filterSpecialChar)#过滤一些中文中夹杂的特殊字符，这些字符容易造成后边df识别出错。

        table.to_csv(r'D:\quantDb\sourceData\gta\data\tables\%s.csv' %dic['TBName'],encoding='utf8')
        tables.append(table)

    df=pd.concat(tables,axis=0)
    df=df.sort_values(['DBTitle','NoteTitle','TBTitle','TBName','Fldname'])
    df=df.reset_index()
    del df['index']
    df.to_csv(r'D:\quantDb\sourceData\gta\data\table2.csv',encoding='utf8')

def toMysql(df,tableName,dbname):
    engine=sqlalchemy.create_engine('mysql+mysqldb://root:root@localhost/%s'%dbname)
    df.to_sql(tableName,engine,if_exists='replace',chunksize=100)
    # df.to_sql(tableName,engine,if_exists='replace',dtype={col:TEXT for col in df.columns},chunksize=100)
    print 'saved %s successfully!'%tableName


# path=r'D:\quantDb\sourceData\gta\data\GTAmenu.csv'
#
#
#
#
# path=u'D:/quantDb/sourceData/gta/data/json1/关联交易情况文件.txt'
#
# dic = json.loads(open(path).read())
# print i, dic['TBName']
# table = json_normalize(dic['TableFieldViewListSet'])
# table['DBTitle'] = dic['DBTitle']
# table['NoteTitle'] = dic['TableView']['NodeTitle']
# table['TBTitle'] = dic['TableView']['TBTitle']
# table['TBName'] = dic['TBName']
# table['url'] = dic['DownSimplePath']
# table['StartTime'] = dic['TableView']['StartTime']
# table['EndTime'] = dic['TableView']['EndTime']
#
# vars = ['DBTitle', 'NoteTitle', 'TBTitle', 'TBName', 'Fldname', 'Title', 'Typename', 'Description', 'StartTime',
#         'EndTime', 'Mergerdatatype', 'url']
# colnames = vars + [col for col in table.columns if col not in vars]
# table = table[colnames]
# # table=table.sort_values(['DBTitle','NoteTitle','TBTitle','TBName','Fldname'])
#
# table['Description'] = table['Description'].apply(_filterSpecialChar)  # 过滤一些中文中夹杂的特殊字符，这些字符容易造成后边df识别出错。
#
#
# table.to_csv(r'e:\aa\aaa.csv',encoding='gbk')
