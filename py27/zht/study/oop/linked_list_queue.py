# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:10:36 2016

@author: Administrator
"""

class Queue:
    def __init__(self):
        self._qhead=None
        self._qtail=None
        self._count=0
    
    def isEmpty(self):
        return self._qhead is None
    
    def __len__(self):
        return self._count
    
    def enqueue(self,item):
        node=_QueueNode(item)
        if self.isEmpty():
            self._qhead=node
        else:
            self._qtail.next=node
        self._qtail=node
        self._count+=1
    
    def dequeue(self):
        assert not self.isEmpty(),'cannot dequeue from an empty queue'
        node=self._qhead
        if self._qhead is self._qtail:
            self._qtail=None
        self._qhead=self._qhead.next
        self._count-=1
        return node.item

class _QueueNode:
    def __init__(self,item):
        self.item=item
        self.next=None

            