#-*-coding: utf-8 -*-
#@author:tyhj

import tushare as ts
import os
import pandas as pd
from Queue import Queue
import threading

df=ts.get_stock_basics()
codes2=df.index.tolist()


files=os.listdir(r'C:\zht\OneDrive\script\rf\stock_monitor\sina')
codes1=[f[:6] for f in files]
codes=[c for c in codes2 if c not in codes1]
codes=sorted(codes)
dir=r'C:\zht\OneDrive\script\rf\stock_monitor\sina'


f=open('codes_abnormal.txt','w')
for code in codes:
    filename=dir+r'\%s.csv'%code
    df = ts.get_h_data(code, start='2005-01-01', end='2016-12-04')  # forward adjusted price
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=None)
    else:
        try:
            df.to_csv(filename)
        except:
            f.write(code+'\n')
    print code

f.close()





'''
f=open('codes_abnormal.txt','w')

q=Queue()
for code in codes:
    q.put(code)

def job(q):
    code=q.get()
    filename=dir+r'\%s.csv'%code
    df = ts.get_h_data(code, start='2005-01-01', end='2016-12-04')  # forward adjusted price
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=None)
    else:
        try:
            df.to_csv(filename)
        except:
            f.write(code+'\n')

    print code

while not q.empty():
    threads=[]
    for i in range(20):
        th=threading.Thread(target=job,args=[q])
        threads.append(th)
    for j in range(len(threads)):
        threads[j].start()
    for k in range(len(threads)):
        threads[k].join()


f.close()

'''




