# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 09:51:16 2016

@author: Administrator
"""

def recBinarySearch(target,theSeq,first,last):
    if first>last:
        return False
    else:
        mid=(last+first)//2
        if theSeq[mid]==target:
            return True
        elif target<theSeq[mid]:
            return recBinarySearch(target,theSeq,first,mid-1)
        else:
            return recBinarySearch(target,theSeq,mid+1,last)
