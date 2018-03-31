# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 11:07:43 2016

@author: hp
"""

import urllib2
import threading
from Queue import Queue

items=[]
lock=threading.Lock()

def fetch_data(y,m):
    global items
    global lock
    url='http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=FD&sty=BST&st=3&sr=true&fd={year}&stat={month}&js=LoadDataResult([(x)])'.format(year=y,month=m)
    content=urllib2.urlopen(url).read()
    data=eval(content.split('(')[1].split(')')[0])
    lock.acquire()
    items+=data
    lock.release()
    print y,m

def run(q):
    global lock
    while not q.empty():
        lock.acquire()
        y,m=q.get()
        lock.release()
        fetch_data(y,m)
        
def multi():
    month=range(1,13)
    year=range(2010,2017)
    q=Queue()
    for y in year:
        for m in month:
            q.put((y,m))
    ts=[]
    for _ in range(10):
        t=threading.Thread(target=run,args=(q,))
        ts.append(t)
        t.start()
    for th in ts:
        th.join()

if __name__=='__main__':
    multi()
    items=sorted(items,key=lambda x:int(x.split(',')[4].replace('-','')))
    with open(r'C:\cq\restricted_share\raw.txt','w') as f:
        f.write('\n'.join(items))
    