# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 19:38:39 2016

@author: Administrator
"""
from array import Array

class SparseMatrix:
    def __init__(self,numRows,numCols):
        self._numCols=numCols
        self._listOfRows=Array(numRows)
    
    def numRows(self):
        return len(self.__listOfRows)
    
    def numCols(self):
        return self._numCols
    
    def __getitem__(self,nudTuple):
        pass
    
    def __setitem__(self,ndxTuple):
        row=ndxTuple[0]
        col=ndxTuple[1]
        predNode=None
        curNode=self._listOfRows[row]
        while curNode is not None and curNode.col!=col:
            preNode=curNode
            curNode=curNode.next
        
        if curNode is not None and curNode.col==col:
            if value==0.0:
                if curNode==self._listOfRows[row]:
                    self._listOfRows[row]=curNode.next
                else:
                    preNode.next=curNode.next
            else:
                curNode.value=value
        elif value!=0.0:
            newNode=_MatrixElementNode(col,value)
            newNode.next==curNode
            if curNode==self._listOfRows[row]:
                self._listOfROws[row]=newNode
            else:
                preNode.next=newNode
    
    def scaleBy(self,scalar):
        for row in range(self.numRows()):
            curNode=self._listOfRows[row]
            while curNode is not None:
                curNode.value*=scalar
                curNode=curNode.next
    
    def transpose(self):
        pass
    
    def __add__(self,rhsMatrix):
        assert rhsMatrix.numRows()==self.numRows() and \
                rhsMatrix.numCols()==self.numCols(), \
                'matrix sizes not compatable for adding.'
        newMatrix=SparseMatrix(self.numROws(),self.numCols())
        for row in range(self.numRows()):
            curNode=self._listOfRows[row]
            while curNode is not None:
                newMatrix[row,curNode.col]=curNode.value
                curNode=curNode.next
            
        for row in range(rhsMatrix.numRows()):
            curNode=rhsMatrix._listOfRows[row]
            while curNode is not None:
                value=newMatrix[row,curNode.col]
                value+=curNode.value
                newMatrix[row,curNode.col]=value
                curNode=curNode.next
        return newMatrix

class _MatrixElementNode:
    def __init__(self,col,value):
        self.col=col
        self.value=value
        self.next=None





    























                
            