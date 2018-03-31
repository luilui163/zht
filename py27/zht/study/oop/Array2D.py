# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 21:46:25 2016

@author: Administrator
"""
from array import *
#if directly using 'from array import Array',it will pop an importError

class Array2D:
    def __init__(self,numRows,numCols):
        self._theRows=Array(numRows)
        for i in range(numRows):
            self._theRows[i]=Array(numCols)
    
    def numRows(self):
        return len(self._thRows)
    
    def numCols(self):
        return len(self._thRows[0])
    
    def clear(self,value):
        for row in range(self.numRows()):
            row.clear(value)
    
    def __getitem__(self,ndxTuple):
        assert len(ndxTuple)==2,'invalid number of array subscripts'
        row=ndxTuple[0]
        col=ndxTuple[1]
        assert row>=0 and row<=self.numRows() \
            and col>=0 and col<=self.numCols(), \
            'array subscripts out of range'
        the1dArray=self._theRows[row]
        return the1dArray[col]

    def __setitem__(self,ndxTuple,value):
        assert len(ndxTuple)==2,'invalid number of array subscripts'
        row=ndxTuple[0]
        col=ndxTuple[1]
        assert row>=0 and row<self.numRows() \
            and col>=0 and col<self.numCols(), \
                'array subscripts out of range.'
        the1dArray=self._theRows[row]
        the1dArray[col]=value
    