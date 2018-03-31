# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 18:40:33 2016

@author: hp
"""
import pandas as pd

def parse_data():
    for name in range(2004,2016):
        url=r'C:\cq\salary\%d.csv'%name
        df=pd.read_csv(url,skiprows=[0,1])
        df=pd.read_csv(r'c:\cq\salary\%d.csv'%name,index_col=0)
        data=df.iloc[1:-2][[1,2,3,8,9]]
        data.columns=['total','director','executive','report_date','annoucement_date']
        f=open(r'C:\cq\salary\%d.txt'%name,'w')
        for i in range(len(data.index)):
            f.write(data.index[i]+'\t')
            for j in range(len(data.columns)):
                f.write(str(data.iat[i,j])+'\t')
            f.write('\n')
        f.close()
        print name

def sh_to_ss():
    for name in range(2004,2016):
        content=open(r'c:\cq\salary\%d.txt'%name).read()
        f=open(r'c:\cq\salary\%d.txt'%name,'w')
        f.write(content.replace('SH','SS').replace('-',''))
        f.close()

parse_data()    
sh_to_ss()