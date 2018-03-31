# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 13:30:41 2016

@author: Administrator
"""
from array import *
from linked_list_queue import Queue

class BPriorityQueue:
    def __init__(self,numLevels):
        self._qSize=0
        self._qLevels=Array(numberLevels)
        for i in range(numberLevels):
            self._qLevels[i]=Queue()
    
    def isEmpty(self):
        return len(self)==0
    
    def __len__(self):
        return len(self._qSize)
    
    def enqueue(self,item ,priority):
        assert priority>=0 and priority<len(self._qLevels), \
            'invalid priority level'
        self._qLevels[priority].enqueue(item)
    
    def dequeue(self):
        assert not self.isEmpty(),'cannot dequeue from an empty queue'
        i=0
        p=len(self._qlevels)
        while i<p and not self._qlevels[i].isEmpty():
            i+=1
        return self._qlevels[i].dequeue()
