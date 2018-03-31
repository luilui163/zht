# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 18:13:48 2016

@author: hp
"""

import urllib2
import os
from bs4 import BeautifulSoup 
import datetime
import json

def get_all_stock_id():
    url=r'http://quote.eastmoney.com/stocklist.html'
    content=urllib2.urlopen(url).read()
    soup=BeautifulSoup(content)
    quote=soup.findAll('div',{'id':'quotesearch'})
    ul=quote[0].findAll('ul')
    li=[]
    for u in ul:
        tmp_li=u.findAll('li')
        li+=tmp_li
    
    sid=[l.string.split('(')[-1][:-1] for l in li]
    sid=[s for s in sid if (s[0]=='0' or s[0]=='3' or s[0]=='6')]
    sid.sort()
    return sid

def spider():
    sids=get_all_stock_id()
    date=datetime.date.today().strftime('%Y%m%d')
    path=r'/dat/datadev/workspace/concept/dongcai'
    if not os.path.isdir(path):
        os.makedirs(path)
    
    f=open(os.path.join(path,date+'.txt'),'w')
    count=0
    for sid in sids:
        url=r'http://app.jg.eastmoney.com/F9Stock/GetConceptBoardList.do?securityCode=%s&yearList=undefined,undefined&dateSearchType=3&=0&rotate=1&seperate=0&order=desc&cashType=0&exchangeValue=0&customSelect=0'%sid
        content=urllib2.urlopen(url).read()
        l=eval(content)
        bk=[]
        for d in l[1:]:
            js=json.loads(json.dumps(d))['BOARDNAME']
            bk.append(js.encode('gbk'))
        f.write(sid+'|')
        f.write('\t'.join(bk)+'\n')
        count+=1
        print count,sid
    f.close()
    
if __name__=='__main__':
    spider()
    