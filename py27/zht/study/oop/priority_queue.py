# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:36:57 2016

@author: Administrator
"""

class PriotityQueue:
    def __init__(self):
        self._qList=list()
    
    def isEmpty(self):
        return len(self)==0
    
    def __len__(self):
        return len(self._qList)
    
    def enqueue(self,item,priority):
        entry=_PriorityQEntry(item,priority)
        self._qList.append(entry)
    
    def dequeue(self):
        assert not self.isEmpty(),'cannot dequeue from an empty queue'
        highest=self._qList[0].priority
        for i in range(1,self.len()):
            if self._qList[i].priority>highest:
                highest=self._qList[i].priority
        entry=self._qList.pop(highest)
        return entry.item

class _PriorityQEntry:
    def __init__(self,item,priority):
        self.item=item
        self.priority=priority
