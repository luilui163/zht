# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 18:13:48 2016

@author: hp
"""

import urllib2
import os
from bs4 import BeautifulSoup 
import datetime
import threading

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

def get_gn(sid):
    date=datetime.date.today().strftime('%Y%m%d')
    path=r'/dat/datadev/workspace/concept/dongcai/%s'%date
    if not os.path.isdir(path):
        os.makedirs(path)
    
    if sid[0]=='6':
        url=r'http://f10.eastmoney.com/f10_v2/OperationsRequired.aspx?code=sh%s'%sid
    else:
        url=r'http://f10.eastmoney.com/f10_v2/OperationsRequired.aspx?code=sz%s'%sid
#    url=r'http://f10.eastmoney.com/f10_v2/OperationsRequired.aspx?code=sh601199'
    content=urllib2.urlopen(url).read().decode('utf-8','replace')
    soup=BeautifulSoup(content)
    
    summary=soup.findAll('div',{'class':'summary'})
    s=summary[0].p
    
    if s.font.string==u'\u6240\u5c5e\u677f\u5757':
        gn=s.contents[2].strip().split(' ')
        if len(gn)!=0:
            f=open(os.path.join(path,sid+'.txt'),'w')
            f.write('\n'.join([g.encode('gbk') for g in gn]))
            f.close()
            print sid


#if __name__=='__main__':
#    sids=get_all_stock_id()
#    for sid in sids:
#        get_gn(sid)

            
sids=get_all_stock_id()

class Consumer(threading.Thread):
    def run(self):
        global sids
        while len(sids)>0:
            sid=sids.pop()
            get_gn(sid)
            
    
if __name__=='__main__':
    for i in range(10):
        Consumer().start()






