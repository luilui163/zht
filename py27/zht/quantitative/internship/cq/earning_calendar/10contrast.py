# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 23:33:20 2016

@author: Administrator
"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import time 

start=time.time()
sharpRatio_f=open(r'c:\earning_calendar\medium\sharpRatio.txt','w')
contrast_sharpRatio_f=open(r'c:\earning_calendar\medium\contrast_sharpRatio.txt','w')
for length in range(3,4,100):
    for number in range(100,101,1000):
#for length in range(1,5,2):
#    for number in range(100,211,20):
        df=pd.read_csv(r'c:\marketAdjustedReturnDF_2004-2016.csv',index_col=0)
        df_date=[d for d in df.index]
        path=r'C:\earning_calendar\quarter'
        files=os.listdir(path)
        filesPath=[os.path.join(path,f) for f in files]
        target_df=pd.DataFrame(np.zeros((len(df),len(df.T))),index=df.index,columns=df.columns)##initialize the target_df
        target_df[target_df==0]=np.nan
        
        contrast_df=pd.DataFrame(np.zeros((len(df),len(df.T))),index=df.index,columns=df.columns)##initialize the target_df
        contrast_df[target_df==0]=np.nan
        
        
        date=[]
        stock=[]
        for i in range(len(filesPath)):
            line=open(filesPath[i]).read().split('\n')[:-1]
            date.extend([int(l[:8]) for l in line][-number:])######
            stock.extend([l[-9:] for l in line][-number:])######
        for k in range(len(stock)):
            col=[s for s in df.columns]
            if stock[k] in col:#确保所选股票在df中
                stock_index=col.index(stock[k])####intersection
                
                for m in range(len(df_date)):
                    if df_date[m]-date[k]<0 and df_date[m+1]-date[k]>=0:
                        mark_date_index=m+1#发布季报后的第一个交易日（包含发布季报的当天）
                        break
                for n in range(mark_date_index,len(df_date)):
                    if str(df.iat[n,stock_index])!='nan':
                        start_date_index=n
                        break
                end_date_index=start_date_index+length
                for g in range(start_date_index,end_date_index):
                    target_df.iat[g,stock_index]=df.iat[g,stock_index]

######发布日期之前持有股票，作为对比
#####################################################################################################
                for m1 in range(len(df_date)):
                    if df_date[m1]-date[k]<0 and df_date[m1+1]-date[k]>=0:
                        contrast_end_date_index=m1+1
                        break
                contrast_start_date_index=contrast_end_date_index-length
                for g1 in range(contrast_start_date_index,contrast_end_date_index):
                    contrast_df.iat[g1,stock_index]=df.iat[g1,stock_index] 
        
        
        
        contrast_df=contrast_df.dropna(axis=1,how='all')
        contrast_df.to_csv(r'C:\earning_calendar\medium\contrast_df\%d_%d.csv'%(length,number))
        returns1=contrast_df.mean(axis=1)
        returns1=returns1.fillna(0)
        cum_sum1=returns1.cumsum()
        std1=returns1.std()
        avg1=returns1.mean()
        sharpRatio1=cum_sum1.values[-1]/std1
        cum_sum1.to_csv(r'c:\earning_calendar\medium\contrast_cumsum_returns\%d_%d.csv'%(length,number))

        contrast_sharpRatio_f.write('%d\t%d\t%f\t%f\t%f\n'%(length,number,avg1,std1,sharpRatio1))        
        
        fig1=plt.figure()
        ax1=fig1.add_subplot(1,1,1)
        ax1.plot(cum_sum1)
        ticks1=ax1.set_xticks([0,242,484,725,967,1213,1475,1699,1934,2186,2424,2669,2913])
        labels1=ax1.set_xticklabels(['2004','2005','2006','2007','2008','20009','2010','2011','2012','2013','2014','2015','2016'],rotation=30,fontsize='small')
#        ax1.set_title('length=%d,number=total,sharpRatio=%f'%(length,sharpRatio1))
        ax1.set_title('length=%d,number=%d,sharpRatio=%f'%(length,number,sharpRatio1))
        fig1.savefig(r'c:\earning_calendar\medium\contrast_fig\%d_%d.png'%(length,number))        
####################################################################################################

        
        
        target_df=target_df.dropna(axis=1,how='all')
        target_df.to_csv(r'C:\earning_calendar\medium\target_df\%d_%d.csv'%(length,number))
        returns=target_df.mean(axis=1)
        returns=returns.fillna(0)
        cum_sum=returns.cumsum()
        std=returns.std()
        avg=returns.mean()
        sharpRatio=cum_sum.values[-1]/std
        cum_sum.to_csv(r'c:\earning_calendar\medium\cumsum_returns\%d_%d.csv'%(length,number))

        sharpRatio_f.write('%d\t%d\t%f\t%f\t%f\n'%(length,number,avg,std,sharpRatio))        
        
        fig=plt.figure()
        ax=fig.add_subplot(1,1,1)
        ax.plot(cum_sum)
        ticks=ax.set_xticks([0,242,484,725,967,1213,1475,1699,1934,2186,2424,2669,2913])
        labels=ax.set_xticklabels(['2004','2005','2006','2007','2008','20009','2010','2011','2012','2013','2014','2015','2016'],rotation=30,fontsize='small')
#        ax.set_title('length=%d,number=total,sharpRatio=%f'%(length,sharpRatio))
        ax.set_title('length=%d,number=%d,sharpRatio=%f'%(length,number,sharpRatio1))
        fig.savefig(r'c:\earning_calendar\medium\fig\%d_%d.png'%(length,number))
        print length,number

sharpRatio_f.close()
contrast_sharpRatio_f.close()

end=time.time()
print end-start
