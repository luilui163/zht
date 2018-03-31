#-*-coding: utf-8 -*-
#@author:tyhj

import os
import pandas as pd

path=r'C:\Users\hp\Desktop\gx_backward'


filenames=os.listdir(path)
for i,filename in enumerate(filenames):
    stockname=filename[3:-4]+'.'+filename[:2]
    columns=['open','high','low','close','volume','amount']
    df=pd.read_csv(path+'\\'+filename,sep='\t',skiprows=[0,1],names=columns,index_col=0)#skip the first 2 rows
    df.drop(df.index[-1],inplace=True)#delete the last row
    ind=df.index
    new_ind=[nd.replace('/','-') for nd in ind]
    df.index=new_ind
    df.to_csv(r'C:\zht\OneDrive\script\rf\stock_monitor\gx_backward\%s.csv'%stockname)
    print i,stockname










