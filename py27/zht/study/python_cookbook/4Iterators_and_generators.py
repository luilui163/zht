# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 17:26:45 2016

@author: hp
"""

class Node:
    def __init__(self,value):
        self._value=value
        self._children=[]
    
    def __repr__(self):
        return 'Node({!r})'.format(self._value)
    
    def add_child(self,node):
        self._children.append(node)
    
    def __iter__(self):
        return iter(self._children)

#Example
if __name__=='__main__':
    root=Node(0)
    child1=Node(1)
    child2=Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print ch
    
    
def frange(start,stop,increment):
    x=start
    while x<stop:
        yield x
        x+=increment

for n in frange(1.0,20,0.01):
    print n
    
f=frange(1,100,10)
print next(f)
print next(f)
print next(f)
print next(f)
print next(f)


class Node:
    def __init__(self,value):
        self._value=value
        self._children=[]
    def __repr__(self,node):
        return 'Node({!r})'.format(self.__value)
    def add_child(self,node):
        self._children.append(node)
    def __iter__(self):
        return iter(self.__children)
    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()


#Iterating in reverse
a=range(2,9)
for x in reversed(a):
    print x


class Countdown:
    def __init__(self,start):
        self.start=start
    
    def __iter__(self):
        n=self.start
        while n>0:
            yield n
            n-=1
    
    def __reversed__(self):
        n=1
        while n<self.start:
            yield n
            n+=1
        

#Iterating over all possible combinations or permutations
items=['a','b','c']
from itertools import permutations
for p in permutations(items):
    print p

for p in permutations(items,2):
    print p

from itertools import combinations
for c in combinations(items,2):
    print c
    

#Iterating over multiple sequences simultaneously
a=[1,2,3]
b=['a','b','c','d','e']
for i in zip(a,b):
    print i
'''
zip(a,b) works by creating an iterator that produces tuples(x,y)
where x is taken from a and y is taken from b.Itration stops whenever
one of the input sequences is exhuasted.Thus,the length of the iteration
is the same as the length of the shortest input.
'''

#Iterating on items in separate containers
from itertools import chain
a=range(1,6)
b=['x','y','z']
for x in chain(a,b):
    print x
    

#Iterating in sorted order over merged sorted iterables
import heapq
a=[1,4,7,10]
b=[2,5,6,11]
for c in heapq.merge(a,b):
    print c
    

