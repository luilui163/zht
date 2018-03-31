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
for length in range(3,55,500):
    for number in range(10,200,5000):
#for length in range(1,5,2):
#    for number in range(100,211,20):
        ###################################################
        returnDF=pd.read_csv(r'c:\returnDF_2004-2016.csv',index_col=0)
        
    
    
    
    
    
        df=pd.read_csv(r'c:\marketAdjustedReturnDF_2004-2016.csv',index_col=0)
        df_date=[d for d in df.index]
        path=r'C:\earning_calendar\quarter'
        files=os.listdir(path)
        filesPath=[os.path.join(path,f) for f in files]
        target_df=pd.DataFrame(np.zeros((len(df),len(df.T))),index=df.index,columns=df.columns)##initialize the target_df
        target_df[target_df==0]=np.nan
        date=[]
        stock=[]
        for i in range(len(filesPath)):
            line=open(filesPath[i]).read().split('\n')[:-1]
            date.extend([int(l[:8]) for l in line][:number])######
            stock.extend([l[-9:] for l in line][:number])######
            
            

        for k in range(len(stock)):
            flag=1###标记，为了达到跳出两层循环的目的   
            
            col=[s for s in df.columns]
            if stock[k] in col:#确保所选股票在df中
                stock_index=col.index(stock[k])####intersection
                for m in range(len(df_date)):
                    if df_date[m]-date[k]<0 and df_date[m+1]-date[k]>=0:
                        mark_date_index=m+1#发布季报后的第一个交易日（包含发布季报的当天）
                        break
                for n in range(mark_date_index,len(df_date)):
                    if str(df.iat[n,stock_index])!='nan':
                        #########需要跳出两层循环
                        if returnDF.iat[n,stock_index]>=0.095 or returnDF.iat[n,stock_index]<=-0.095:###############
                            flag=0
                            break
                        else:
                            start_date_index=n
                            break
                if flag!=0:##########
                    if start_date_index+length<=len(df.T):
                        end_date_index=start_date_index+length
                    else:
                        end_date_index=len(df.T)
                    for g in range(start_date_index,end_date_index+1):#########+1
                        target_df.iat[g,stock_index]=df.iat[g,stock_index]
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
        ax.set_title('length=%d,number=%d,sharpRatio=%f'%(length,number,sharpRatio))
#        ax.set_title('length=%d,number=all,sharpRatio=%f'%(length,sharpRatio))
#        fig.savefig(r'c:\earning_calendar\medium\fig\%d_all.png'%(length))
        fig.savefig(r'c:\earning_calendar\medium\fig\%d_%d.png'%(length,number))
        print length,number

sharpRatio_f.close()

end=time.time()
print end-start

