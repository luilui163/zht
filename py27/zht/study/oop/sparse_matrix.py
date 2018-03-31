# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 18:50:03 2016

@author: Administrator
"""
class SparseMatrix:
    def __init__(self,numRows,numCols):
        self._numRows=numRows
        self._numCols=numCols
        self._elementList=list()
        
    def numRows(self):
        return self._numRows
    
    def numCols(self):
        return self._numCols
        
    def __getitem__(self,ndxTuple):
        ndx=self._findPosition(ndxTuple[0],ndxTuple[1])
        if ndx is not None:
            return self._elementList[ndx].value
        else:
            return 0.0
    
    def __setitem__(self,ndxTuple,scalar):
        ndx=self._findPosition(ndxTuple[0],ndxTuple[1])
        if ndx is not None:
            if scalar!=0.0:
                self._elementList[ndx].value=scalar
            else:
                self._elementList.pop(ndx)
        else:
            if scalar!=0.0:
                element=_MatrixElement(ndxTuple[0],ndxTuple[1],scalar)
                self._elementList.append(element)
                
    def scaleBy(self,scalar):
        for element in self._elementList:
            element.value*=scalar
    
#    def __add__(self,rhsMatrix):
#        newMatrix=SparseMatrix(self.numRows,self.numCols)
#        for r in range(self.numRows):
#            for c in range(self.numCols):
#                newMatrix[r,c]=self[r,c]+rhsMatrix[r,c]
#        return newMatrix

    def __add__(self,rhsMatrix):
        assert rhsMatrix.numRows()==self.numRows and \
               rhsMatrix.numCols()==self.numCols, \
               'matrix sizes not compatible for the add operation'
        newMatrix=SparseMatrix(self.numCols(),self.numCols())
        
        for element in self._elementList:
            dupElement=_MatrixElement(element.row,element.col,element.value)
            newMatrix._elementList.append(dupElement)
        
        for element in rhsMatrix._elemenList:
            value=newMatrix[element.row,element.col]
            value+=element.value
            newMatrix[element.row,element.col]=value
        return newMatrix
    
    def _findPosition(self,row,col):
        n=len(self._elementList)
        for i in range(n):
            if self._elementList[i].row==row and \
                self._elementList[i].col==col:
                return i
        return None
    
class _MatrixElement:
    def __init__(self,row,col,value):
        self.row=row
        self.col=col
        self.value=value












            