# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 16:34:30 2016

@author: Administrator
"""
class Bag:
    def __init__(self):
        self._head=None
        self._size=0
        
    def __len__(self):
        return self._size
    
    def __contains__(self,target):
        curNode=self._head
        while curNode is not None and curNode.item!=target:
            curNode=curNode.next
        return curNode is not None
    
    def add(self,item):
        newNode=_BagListNode(item)
        newNode.next=self._head
        self._head=newNode
        self._size+=1
    
    def remove(self,item):
        preNode=None
        curNode=self._head
        while curNode is not None and curNode.item!=item:
            preNode=curNode            
            curNode=curNode.next
        assert curNode is not None,'the item must be in the bag'
        self._size_=1
        if curNode is self._head:
            self._head=curNode.next
        else:
            preNode.next=curNode.next
        return curNode.item
        
#    def __iter__(self):
#        return _BagIterator(self.__head)

class _BagListNode:
    def __init__(self,item):
        self.item=item
        self.next=None

class _BagIterator:
    def __init__(self,listHead):
        self._curNode=listHead
    
    def __iter__(self):
        return self
    
    def next(self):
        if self._curNOde is None:
            raise StopIteration
        else:
            item=self._curNOde.item
            self._curNode=self._curNode.next
            return item













            