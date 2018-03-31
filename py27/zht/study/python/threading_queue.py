# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 09:23:05 2016

@author: hp
"""
'''
这个模型也叫生产者-消费者模型
'''

import Queue
import threading

message=Queue.Queue(10)

def producer(i):
    while True:
        message.put(i)

def consumer(i):
    while True:
        message.get()
    
for i in range(12):
    t=threading.Thread(target=producer,args=(i,))
    t.start()
    
for j in range(10):
    t=threading.Thread(target=consumer,args=(i,))
    t.start()