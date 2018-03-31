# -*- coding: utf-8 -*-
"""
Created on Wed Jul 06 13:53:12 2016

@author: 13163
"""
import pandas as pd
import numpy as np
import os

dir_name=r'C:\cq\concept\wind_formatted\data'
file_names=os.listdir(dir_name)
file_paths=[os.path.join(dir_name,fn) for fn in file_names]
dates=[fn[:-4] for fn in file_names]



return_df=pd.read_csv(r'c:\cq\return_df.csv',index_col=0)
tmp_f=open(r'c:\cq\concept\wind_formatted\concept_name.txt').read().split('\n')[:-1]
concept_codes=[tf.split('\t')[0] for tf in tmp_f]

index_return_df=pd.DataFrame(np.zeros((len(dates),len(concept_codes))),index=dates,columns=concept_codes)
index_return_df[index_return_df==0]=np.nan

#file_path=file_paths[0]
#date=dates[0]

return_df_stocks=list(return_df.columns)

for p in range(len(file_paths)):
    file_path=file_paths[p]
    date=dates[p]
    
    lines=open(file_path).read().split('\n')[:-1]

    concepts=[]
    for l in lines:
        tmp_concepts=l.split('\t')[1:]
        for tc in tmp_concepts:
            if tc not in concepts:
                concepts.append(tc)
                
    for c in concepts:
        stocks=[]
        for l in lines:
            if c in l.split('\t') and l.split('\t')[0] in return_df_stocks:
                stocks.append(l.split('\t')[0])
                
        returns=[]
        for s in stocks:
            if not np.isnan(return_df.at[int(date),s]):
                returns.append(return_df.at[int(date),s])
        returns_arr=np.array(returns)
        avg=returns_arr.mean()
        index_return_df.at[date,c]=avg
    print p,date

index_return_df.to_csv(r'c:\garbage\wind\index_return_df.csv')