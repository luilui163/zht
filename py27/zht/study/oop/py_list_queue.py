# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 10:01:20 2016

@author: Administrator
"""

class Queue:
    def __init__(self):
        self._qList=list()
    
    def isEmpty(self):
        return len(self._qList)==0
    
    def __len__(self):
        return len(self.__qList)
    
    def enqueque(self,item):
        self._qList.append(item)
    
    def dequeue(self,item):
        assert not self.isEmpty(),'cannot dequeue from an empty queue'
        return self._qList.pop(0)
    
