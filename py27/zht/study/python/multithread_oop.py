# -*- coding: utf-8 -*-
"""
Created on Fri Aug 05 22:23:52 2016

@author: hp
"""
import threading
import time
import os
import random

def job():
    interval=random.random()
    time.sleep(interval)

class BoothThread(threading.Thread):
    def __init__(self,monitor,tid):
        threading.Thread.__init__(self)
        self.monitor=monitor
        self.tid=tid    
    
    def run(self):
        while True:
            monitor['lock'].acquire()
            if monitor['tick']!=0:
                monitor['tick']-=1
                print self.tid,'now,tick is:',monitor['tick']
                job()
            else:
                print self.tid,'no more tick'
                os._exit(0)
            monitor['lock'].release()
            
if __name__=='__main__':
    monitor={'tick':100,'lock':threading.Lock()}
    for i in range(1,13):
        b=BoothThread(monitor,i)
        b.start()
        