# -*- coding: utf-8 -*-
"""
Created on Wed Aug 03 23:46:24 2016

@author: hp
"""

import threading
import time
from Queue import Queue

def job(l,q):
    for i in range(len(l)):
        l[i]*=l[i]
    q.put(l)

def multithreading():
    q=Queue()
    data=[[1,2,4],[3,5,7],[6,3,10]]
    threads=[]
    for i in range(3):
        th=threading.Thread(target=job,args=[data[i],q])
        threads.append(th)
    for j in range(len(threads)):
        threads[j].start()
    for k in range(len(threads)):
        threads[k].join()
    for i in range(len(data)):
        print q.get()

if __name__=='__main__':
    multithreading()