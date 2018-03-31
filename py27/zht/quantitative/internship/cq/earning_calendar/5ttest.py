# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 22:57:38 2016

@author: Administrator
"""
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import os



def ttest(path):
    files=os.listdir(path)
    filesPath=[os.path.join('%s\%s'%(path,f)) for f in files]
    f=open(r'C:\earning_calendar\result\ttest_%s.txt'%path.split('\\')[-1],'w')
    
    
    namelist=[0]*len(filesPath)
    avglist=[0]*len(filesPath)
    plist=[0]*len(filesPath)
    for k in range(len(filesPath)):
    #    p=r'C:\earning_calendar\result\early\early_length=1_number=10.txt'
        line=open(filesPath[k]).read().split('\n')
        returns=[0]*(len(line)-1)
        zero=[0]*(len(line)-1)
        for i in range(len(line)-1):
            returns[i]=float(line[i].split('\t')[1])
        df=pd.DataFrame({'returns':returns,'zero':zero})
        (t,p)=ttest_ind(df.iloc[:,0],df.iloc[:,1])
        returnsArr=np.array(returns)
        avg=returnsArr.mean()
        f.write('%s\t%f\t%f\n'%(files[k][:-4],avg,p))
        
        namelist[k]=files[k][:-4]
        avglist[k]=avg
        plist[k]=p
    f.close()
    return(namelist,avglist,plist)
    
path1=r'C:\earning_calendar\result\early'
path2=r'C:\earning_calendar\result\late'
(namelist1,avglist1,plist1)=ttest(path1)
(namelist2,avglist2,plist2)=ttest(path2)
for m in range(len(namelist1)):
    if plist1[m]<=0.05:
        

    
    
    
    
    