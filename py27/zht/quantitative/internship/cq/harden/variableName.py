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


(filePathList,fileNameList)=getAllFilePath('d:\\bloomberg')


#print len(dict)
#print len(fileNameList)


#print filePathList[2406]
#print filePathList[2405]

#print len(dict)
#print len(fileNameList)

#print dict[100][100][0]
#print dict[100][100][1]
print fileNameList[2584]
print fileNameList[2585]


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    