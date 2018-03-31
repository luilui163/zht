# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 10:41:16 2016

@author: Administrator

说明，涨停是以每日的收盘价来判断的
"""

import os
import numpy as np


def  getAllFilePath(path):  #三层目录
    fileNameList=[]
    filePathList=[]
    firstClassFolderName=os.listdir(path)
    #print firstClassFolderName

    for i in firstClassFolderName:
        firstClassPathName=os.path.join('%s\%s'%(path,i))
       # print firstClassPathName
        secondClassFolderName=os.listdir(firstClassPathName)
        for j in  secondClassFolderName:
            secondClassPathName=os.path.join('%s\%s'%(firstClassPathName,j))
            for fileName in os.listdir(secondClassPathName):
                #print fileName
                filePath=os.path.join('%s\%s'%(secondClassPathName,fileName))
                fileNameList.append(fileName)
                filePathList.append(filePath)
    return (filePathList,fileNameList)
    #print len(filePathList)
    #print len(fileNameList)
    #print fileNameList


'''
def getNameAndPrice(filePathList,fileNameList):
    fileList=['']*len(filePathList)
    dateList=['']*len(fileNameList)
    nameList=['']*len(fileNameList)
    for i in range(len(filePathList)):
        dateList[i]=fileNameList[i].replace('.','')[-8:]
    #    print dateList[i]+'price'
    #    print dateList[i]+'name'
    #print dateList
    #print len(dateList)
        
        fileList[i]=open(filePathList[i])
        lineList=fileList[i].read().split('\n')
    
        nameList[i]t=['']*(len(lineList)-1)
        priceList[i]=['']*(len(lineList)-1)
        for j in range(len(line)-1):
            name[i]=line[i].split(',')[3]
            price[i]=line[i].split(',')[4]
            print
'''
def getNameAndPrice(filePath):
    line=open(filePath).read().split('\n')
    name=['']*(len(line)-1)
    price=['']*(len(line)-1)
    for i in range(len(line)-1):
        name[i]=line[i].split(',')[3]
        price[i]=line[i].split(',')[4]
    #return (name,price)
    return dict(zip(name,price))

def findNewStock(name1,name2):
    return list(set(name2).difference(set(name1)))
    
def findOldStock(name1,name2):
    return list(set(name2).intersection(set(name1)))

def findIpoStockNameList(nameList,n):#用来寻找到n-1天为止，出现过的股票，这些不是第n天的ipo股票
    tmp=nameList[n-1]
    for i in range(len(nameList)-1):
        tmp=list(set(tmp).union(set(nameList[i])))
    return list(nameList[n-1].difference(set(tmp)))

def findHardenStock(ipoStockNameList):
    number=len(ipoStockNameList)
    ipoStockPrice=price.index()


    
    


file=getAllFilePath('d:\\bloomberg')
getNameAndPrice(filePathList,fileNameList)