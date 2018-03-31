# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 20:07:59 2016

@author: Administrator
"""
class Stack:
    def __init__(self):
        self._theItems=list()
    
    def isEmpty(self):
        return len(self)==0
    
    def __len__(self):
        return len(self._theItems)
    
    def peek(self):
        assert not self.isEmpty(),'cannot peek from an empty stack'
        return self._theItems[-1]
    
    def pop(self):
        assert not self.isEmpty(),'cannot pop from an empty stack'
        
    def push(self,item):
        self._theItems.append(item)















