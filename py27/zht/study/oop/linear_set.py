# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 16:51:55 2016

@author: Administrator
"""

class Set:
    def __init__(self):
        self._the_elements=list()
    
    def __len__(self):
        return len(self._the_elements)
    
    def __contains__(self,element):
        return element in self._the_elements
    
    def add(self,element):
        if element not in self:
            self._the_elements.append(element)
    
    def remove(self,element):
        assert element in self,'the element is not in the set.'
        self._the_elements.remove(element)
    
    def __eq__(self,setB):
        if len(self)!=len(setB):
            return False
        else:
            return self.is_subset_of(setB)

    def is_subset_of(self,setB):
        for element in self:
            if element not in setB:
                return False
        return True

    def union(self,setB):
        new_set=Set()
        new_set._the_elements.extend(self._the_elements)
        for element in setB:
            if element not in self:
                new_set._elements.append(element)
        return new_set



