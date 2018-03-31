# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 20:13:20 2016

@author: Administrator
"""

class Stack:
    def __init__(self):
        self._top=None
        self._size=0
    
    def isEmpty(self):
        return self._top is None
    
    def __len__(self):
        return self._size
    
    def peek(self):
        assert not self.isEmpty(),'cannot peek at an empty stack'
    
    def pop(self):
        assert not self.isEmpty(),'cannot pop from an empty stack'
        node=self._top
        self._top=self._top.next
        self._size-=1
        return node.item
    
    def push(self,item):
        self._top=_StackNode(item,self._top)
        self._size+=1
    
class _StackNode:
    def __init__(self,item,link):
        self.item=item
        self.next=link

#implementation of the algorithm for validating balanced brackets in
#an C++ source file.

def isValidSource(srcfile):
    s=Stack()
    for line in srcfile:
        for token in line:
            if token in '{[(':
                s.push(token)
            elif token in '}])':
                if s.isEmpty:
                    return False
                else:
                    left=s.pop()
                    if (token=='}' and left!='{') or \
                        (token==']' and left!='[') or \
                        (token==')' and left!='('):
                        return False
    return s.isEmpty()



