# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 23:33:20 2016

@author: Administrator
"""
import pandas as pd
import numpy as np
from sklearn import covariance,cluster
import time

start=time.time()

openprice=pd.read_csv(r'c:\cluster\openprice_df.csv',index_col=0)
closeprice=pd.read_csv(r'c:\cluster\closeprice_df.csv',index_col=0)
var=closeprice-openprice
std=var.std()
x=var/std
x=x.fillna(0)
x=x.iloc[:,:100]
edge_model=covariance.GraphLassoCV()
edge_model.fit(x)
_,labels = cluster.affinity_propagation(edge_model.covariance_)
n_labels=labels.max()


#for i in range(n_labels+1):
#    print ('cluster %i:%s'%((i+1),','.join(var.columns[labels==i])))
#for j in range(n_labels+1):
#    for i in range(len([l for l in var.columns[labels==j]])):
#        result.iat[i,j]=var.columns[labels==j][i]
        
#result=pd.DataFrame({'cluster%d'%i:var.columns[labels==i] for i in range(n_labels+1)})
for i in range(n_labels+1):
    f=open(r'c:\cluster\result\%d.txt'%i,'w')
    for j in range(len(var.columns[labels==i])):
        f.write('%s\n'%var.columns[labels==i][j])
    f.close()
#result.to_csv(r'C:\cluster\retult.csv')

end=time.time()
print end-start










    
    
    
    
    
    
    
    
    
    