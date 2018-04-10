# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-04-10  14:08
# NAME:zht-get_dbid.py

import os

import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import json

PATH=r'D:\zht\database\quantDb\sourceData\gta\20180410\crawler'

def get_seriesids():
    url = 'http://www.gtarsc.com/SingleTable/Index?nodeid=479'
    response = urlopen(url)
    content = response.read()

    soup = BeautifulSoup(content, 'lxml')

    _lis = soup.findAll('li', {'seriesid': True})

    items = []
    for _li in _lis:
        seriesid = _li['seriesid']
        name = _li.text
        items.append((seriesid, name))
    return items

def get_nodeid(seriesid):
    url = 'http://www.gtarsc.com/SingleTable/GetDataBase?seriesid={}'.format(seriesid)
    response=urlopen(url)
    content=response.read()

    soup=BeautifulSoup(content,'lxml')

    _as=soup.findAll('a',{'target':'_parent'})

    items=[]
    for _a in _as:
        nodeid=_a['href'].split('=')[1]
        name=_a.text
        items.append((name,nodeid))

    return pd.DataFrame(items,columns=['name','nodeid'])

def get_part_of_nodeid():
    seriesids=get_seriesids()
    df=pd.concat([get_nodeid(s[0]) for s in seriesids],axis=0,keys=[s[0]+'__'+s[1] for s in seriesids])
    df.index.names=['series','tmp']
    df=df.reset_index('tmp',drop=True)
    return df


def _get_all_nodeid_and_tbid(nodeid):
    url=r'http://www.gtarsc.com/SingleTable/DataBaseInfo?nodeid={}'.format(nodeid)
    response = urlopen(url)
    content = response.read()
    soup = BeautifulSoup(content, 'lxml')
    _lis= soup.findAll('li', {'codetype':True,'nodeid':True,'nodename':True})
    items=[]
    for _li in _lis:
        nodeid=_li['nodeid']
        tbid=_li['tbid']
        items.append((nodeid,tbid))

    df=pd.DataFrame(items,columns=['nodeid','tbid'])
    time.sleep(0.2)
    return df

def get_nodeid_tbid():
    df=get_part_of_nodeid()
    _dfs=[]
    for i,nodeid in enumerate(df['nodeid']):
       _dfs.append(_get_all_nodeid_and_tbid(nodeid))
       print(i,nodeid)

    comb=pd.concat(_dfs,axis=0)
    comb.to_csv(os.path.join(PATH,'nodeid_tbid.csv'))
    return comb

def get_json(update=False):
    def _func(url,nodeid,tbid):
        response=urlopen(url)
        content = response.read()
        js = json.loads(content)
        with open(os.path.join(PATH, 'json', '{}_{}.txt'.format(nodeid, tbid)), 'w') as f:
            json.dump(js, f)

    if update:
        comb=get_nodeid_tbid()
    else:
        comb = pd.read_csv(os.path.join(PATH, 'nodeid_tbid.csv'), index_col=0)

    for i in range(comb.shape[0]):
        time.sleep(0.1)
        nodeid=comb['nodeid'].values[i]
        tbid=comb['tbid'].values[i]
        url=r'http://www.gtarsc.com/SingleTable/TreeNodeSelected?treeNodeId={}&projectId=null&tbId={}'.format(nodeid,tbid)
        try:
            _func(url,nodeid,tbid)
        except:
            refuse=True
            while refuse:
                try:
                    _func(url,nodeid,tbid)
                    refuse=False
                except:
                    print('refused!')
                    time.sleep(2)
        print(i, nodeid, tbid)


if __name__=='__main__':
    get_json()