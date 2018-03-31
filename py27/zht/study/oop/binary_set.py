# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 23:52:43 2016

@author: Administrator
"""
class Set:
    def __init__(self):
        self._theElements=list()
    
    def __len__(self):
        return len(self._theElements)
    
    def __contains__(self,element):
        ndx=self._findPosition(element)
        return ndx<len(self) and self._theElements[ndx]==element
    
    def remove(self,element):
        assert element in self,'the element must be in the set'
        ndx=self._findPosition(element)
        self._theElements.pop(ndx)
    
    def isSubsetOf(self,setB):
        for element in self:
            if element not in setB:
                return False
        return True
    
#    def __eq__(self,setB):
#        if len(self)!=len(setB):
#            return False
#        else:
#            return self.isSubsetOf(setB)
    
    def __eq__(self,setB):
        if len(self)!=len(setB):
            return False
        else:
            for i in range(len(self)):
                if self._theElements[i]!=setB._theElements[i]:
                    return False
            return True
    
    def union(self,setB):
        newSet=Set()
        a=0
        b=0
        while a<len(self) and b<len(setB):
            valueA=self._theElements[a]
            valueB=setB._theElements[b]
            if valueA<valueB:
                newSet._theElements.append(valueA)
                a+=1
            elif valueA>valueB:
                newSet._theElements.append(valueB)
                b+=1
            else:
                newSet._theElements.append(valueA)
                a+=1
                b+=1
        while a<len(self):
            newSet._theElements.append(self._theElements[a])
            a+=1
        while b<len(setB):
            newSet._theElements.append(setB._theElements[b])
            b+=1
        return newSet

    
    def __iter__(self):
        return _SetIterator(self._theElements)
    
    def _findPosition(self,element):
        low=0
        high=len(self)-1
        while low<high:
            mid=(high+low)/2
            if element==self._theElements[mid]:
                return mid
            elif element<self._theElements[mid]:
                high=mid-1
            else:
                low=mid+1
        return low
