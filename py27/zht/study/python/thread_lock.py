# -*- coding: utf-8 -*-
"""
Created on Thu Aug 04 00:13:40 2016

@author: hp
"""

#import threading
#
#def fun1():
#    global a
#    for i in range(9):
#        a+=1
#        print 'fun1',a
#
#def fun2():
#    global a
#    for i in range(9):
#        a+=10
#        print 'fun2',a
#
#
#if __name__=='__main__':
#    a=0
#    th1=threading.Thread(target=fun1)
#    th2=threading.Thread(target=fun2)
#    th1.start()
#    th2.start()
#    th1.join()
#    th2.join()

import threading

def fun1():
    global a,glock
    glock.acquire()
    for i in range(9):
        a+=1
        print 'fun1',a
    glock.release()
    
    
def fun2():
    global a,glock
    glock.acquire()
    for i in range(9):
        a+=10
        print 'fun2',a
    glock.release()

if __name__=='__main__':
    a=0
    glock=threading.Lock()
    th1=threading.Thread(target=fun1)
    th2=threading.Thread(target=fun2)
    th1.start()
    th2.start()
    th1.join()
    th2.join()
    
