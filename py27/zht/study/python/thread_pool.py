# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 09:30:51 2016

@author: hp
"""

import threading
import time
import Queue

class Thread_pool():
    def __init__(self,q_size=5):
        self.q=Queue.Queue(q_size)
        for _ in range(q_size):
            self.add_thread()
    
    def add_thread(self):
        self.q.put(threading.Thread)
    
    def get_thread(self):
        return self.q.get()
    

def fun(thread_pool,i):
    time.sleep(1)
    print i
    thread_pool.add_thread()

if __name__=='__main__':
    thread_pool=Thread_pool(10)
    for i in range(20):
        thread=thread_pool.get_thread()
        t=thread(target=fun,args=(thread_pool,i))
        t.start()
