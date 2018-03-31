# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 09:45:40 2016

@author: hp
"""

import greenlet
 
def fun1():
    for i in range(10,200,20):
        print 'fun1:',i
        g2.switch()

def fun2():
    for j in range(2,11,2):
        print 'fun2:',j
        g1.switch()

g1=greenlet.greenlet(fun1)
g2=greenlet.greenlet(fun2)
g1.switch()



import random
from greenlet import greenlet
from Queue import Queue
import time

q=Queue()

@greenlet
def producer():
    l=list('qwertyuiopasdfghjklzxcvbnm')
    while True:
        char=random.choice(l)
        q.put(char)
        print 'produce:',char
        time.sleep(0.3)
        consumer.switch()


@greenlet
def consumer():
    while True:
        if q.empty():
            producer.switch()
        else:
            char=q.get()
            print 'consume:',char
            time.sleep(0.5)
            producer.switch()

if __name__=='__main__':
#    producer.run()
    consumer.run()

