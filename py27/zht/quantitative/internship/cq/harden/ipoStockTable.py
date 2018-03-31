# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 13:42:44 2016

@author: Administrator
"""

import os
import numpy as np
import time
import sys
start=time.time()

reload(sys)
sys.setdefaultencoding('utf-8')

def  getAllFilePath(path):  #三层目录c
    fileNameList=[]
    filePathList=[]
    firstClassFolderName=os.listdir(path)
    for i in firstClassFolderName:
        firstClassPathName=os.path.join('%s\%s'%(path,i))
        secondClassFolderName=os.listdir(firstClassPathName)
        for j in  secondClassFolderName:
            secondClassPathName=os.path.join('%s\%s'%(firstClassPathName,j))
            for fileName in os.listdir(secondClassPathName):
                filePath=os.path.join('%s\%s'%(secondClassPathName,fileName))
                fileNameList.append(fileName)
                filePathList.append(filePath)
    return (filePathList,fileNameList)


def getNameListAndPriceList(filePath):
    line=open(filePath).read().split('\n')
    nameList=['']*(len(line))
    priceList=['']*(len(line))
    #某些数据后边有两个\n,有些数据最后边只有一个\n
    tmp=len(line)-1
    while True:
        if line[tmp]=='':
            del line[tmp]
            tmp-=1
        else:
            break
        
    for i in range(len(line)):
        nameList[i]=line[i].split(',')[3]
        priceList[i]=line[i].split(',')[4]
    #return (name,price)
    #某些name和price的最后一个数据为空或99999，此处将其处理
    tmp2=len(line)-1
    while True:
        if nameList[tmp2]=='99999' or nameList[tmp2]=='':
            del nameList[tmp2]
            del priceList[tmp2]
            tmp2-=1
        else:
            break
    #待解决问题，最后一个元素为''好像还是没解决（99999已经去除）
    return (nameList,priceList)
    
    

(filePathList,fileNameList)=getAllFilePath('d:\\bloomberg')


'''
def findNewStock(name1,name2):
    return list(set(name2).difference(set(name1)))
'''   
def getNameTableAndPriceTable(filePathList):
    nameTable=[[0 for j in range(5000)] for i in range(len(fileNameList))]
    priceTable=[[0 for j in range(5000)] for i in range(len(fileNameList))]
    for i in range(len(filePathList)):
        (nameTable[i],priceTable[i])=getNameListAndPriceList(filePathList[i])
    return( nameTable,priceTable)

(nameTable,priceTable)=getNameTableAndPriceTable(filePathList)#nameTable[i][j],i is the index of someday,j is the index of stock

def getNewStock(name1,name2):
    return list(set(name2).difference(set(name1)))
def getOldStock(name1,name2):
    return list(set(name2).union(set(name1)))
    
def getIpoStockTable(nameTable):
    newStockTable=[[0 for j in range(5000)]for i in range(len(nameTable))]
    oldStockTable=[[0 for j in range(5000)]for i in range(len(nameTable))]
    ipoStockTable=[[0 for j in range(5000)]for i in range(len(nameTable))]
    oldStockTable[0]=nameTable[0]
    #mark=0
    for i in range(1,len(nameTable)):
        newStockTable[i]=getNewStock(nameTable[i-1],nameTable[i])
        oldStockTable[i]=list(nameTable[i-1])
        oldStockTable[i].extend(newStockTable[i])
        ipoStockTable[i]=list(set(newStockTable[i]).difference(set(oldStockTable[i-1])))
    #return (newStockTable,oldStockTable,ipoStockTable)
    return ipoStockTable
ipoStockTable=getIpoStockTable(nameTable)
#注意，此处没有排除数据中非股票数据，还需要限定为0,3,6开头的数据
for i in range(len(ipoStockTable)):
    if len(ipoStockTable[i])!=0:
        print fileNameList[i]
        print ipoStockTable[i]


    


end=time.time()
timelenght=end-start
print timelenght
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    