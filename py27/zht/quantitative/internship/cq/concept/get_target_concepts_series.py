# -*- coding: utf-8 -*-
"""
Created on Mon Jul 04 16:33:56 2016

@author: 13163
"""

import pandas as pd

ma=10
ratio=0.05
#
#index_return_df=pd.read_csv(r'c:\garbage\wind\index_return_df.csv',index_col=0)
#index_rolling_return_std_df=pd.rolling_std(index_return_df,ma)
#index_rolling_return_std_df.to_csv(r'c:\garbage\wind\index_rolling_return_std_df.csv')
#

#

df=pd.read_csv(r'c:\garbage\wind\index_df.csv',index_col=0)
concept_number=len(df.columns)
target_number=int(concept_number*ratio)

concepts_list=[]
for i in range(len(df.index)):
    tmp_row=df.iloc[i]
    row_list=list(tmp_row)
    
    target_concept=[]
    for t in range(target_number):
        tmp_max=max(row_list)
        tmp_index=row_list.index(tmp_max)
        target_concept.append(df.columns[tmp_index])
        row_list.remove(tmp_max)
    concepts_list.append(target_concept)


f=open(r'c:\garbage\wind\target_concepts.txt','w')
for j in range(len(concepts_list)):
    f.write('%d\t'%df.index[j])
    for k in range(len(concepts_list[j])-1):
        f.write('%s\t'%concepts_list[j][k])
    f.write('%s\n'%concepts_list[j][k+1])
f.close()

'''
注意target_concepts.txt中的第一行全部是一样的，是无效数据，从第二行开始才有效
'''

















