import os
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

start=time.time()


#path=r'C:\industry_change\zx'
#
#files=os.listdir(path)
#files_paths=[os.path.join(path,f) for f in files]
#files_paths=sorted(files_paths)


def handle_one_file(file_number,files_paths):
    i=file_number
    date=0
    lines=open(files_paths[i]).read().split('\n')[:-1]
    stock=files_paths[i].split('_')[2][-9:]
    for j in range(1,len(lines)):
#        date0=lines[j-1].split('\t')[0]
        industry0=lines[j-1].split('\t')[1].split('-')[2]
        date1=lines[j].split('\t')[0]
        industry1=lines[j].split('\t')[1].split('-')[2]
        if industry1!=industry0:
            date=date1
            break
    return (stock,date,industry0,industry1)

def get_stocks_and_dates():
    path=r'C:\industry_change\zx_new'
    files=os.listdir(path)
    files_paths=[os.path.join(path,f) for f in files]
    files_paths=sorted(files_paths)
    
    stocks=[]
    dates=[]
    industrys0=[]
    industrys1=[]
    for m in range(len(files_paths)):
        (stock,date,industry0,industry1)=handle_one_file(m,files_paths)
        stocks.append(stock)
        dates.append(date)
        industrys0.append(industry0)
        industrys1.append(industry1)
    return (stocks,dates,industrys0,industrys1)

(stocks,dates,industrys0,industrys1)=get_stocks_and_dates()

#def get_target_stocks(stocks,dates,indsutrys1):
#    target_stocks=[]
#    target_dates=[]
#    path=r'C:\bloomberg_new\df_of_everyday'
#    files=os.listdir(path)
#    df_dates=[f[:-4] for f in files]
#    df_dates=sorted(df_dates)
#    for i in range(len(stocks)):
#        mark=0
#        for d in range(len(df_dates)):
#            if int(dates[i])>int(df_dates[d]) and int(dates[i])<=int(df_dates[d+1]):
#                mark=d
#                break
#        if mark:
#            df=pd.read_csv(r'C:\bloomberg_new\df_of_everyday\%s.csv'%df_dates[d],index_col=0)
#            target_df=df[['returns','zx3']]
#            industry=industrys1[i]
#            market_avg_return=df.mean().values[0]
#            mm=target_df[target_df.zx3==industry]
#            industry_avg_return=mm.mean().values[0]
#            index_list=[k for k in df.index]
#            if stocks[i] in index_list:
##                index_number=index_list.index(stocks[i])
##                stock_return=df.returns[index_number]
#
#                if industry_avg_return>market_avg_return and df.loc[stocks[i],'returns']>industry_avg_return:#########选股条件
#                    target_stocks.append(stocks[i])
#                    target_dates.append(dates[i])
#            print i
#    return (target_stocks,target_dates)
#
#(target_stocks,target_dates)=get_target_stocks(stocks,dates,industrys1)

def get_pnl(stocks,dates,length,time_model=1):
    #time_model   -1 for before    1 for after
    df=pd.read_csv(r'c:\returnDF_2004-2016.csv',index_col=0)
    market_return=df.mean(axis=1)
    df_index=[i for i in df.index]
    df_col=[c for c in df.columns]
    #target_df=pd.DataFrame(np.nan((len(df),len(df.T))),index=[i for i in df.index],columns=[c for c in df.columns])
    target_df=df.copy()
    target_df[target_df>-9999999]=np.nan
    for i in range(len(stocks)):
        if dates[i]!=0:
            index=df_index.index(int(dates[i]))
            col=df_col.index(stocks[i])
            if abs(df.iat[index,col])<=0.095 and df.iat[index-2,col]+df.iat[index-1,col]<0:
                for k in range(index,index+length):
                    target_df.iat[k,col]=df.iat[k,col]-market_return.values[k]
            elif abs(df.iat[index,col])<=0.095 and df.iat[index-2,col]+df.iat[index-1,col]>0:
                for k in range(index,index+length):
                    target_df.iat[k,col]=-df.iat[k,col]+market_return.values[k]
#                if time_model==1:
#                    for k in range(index,index+length):
#                        target_df.iat[k,col]=-df.iat[k,col]+market_return.values[k]
#    target_df.to_csv(r'C:\industry_change\%d.csv'%length)
    pnl=target_df.mean(axis=1)
    return pnl

def draw(pnl,length,time_model=1):
    pnl=pnl.fillna(0)
    std=pnl.std()
    avg=pnl.mean()
    pnl.to_csv(r'c:\industry_change\pnl_%d.csv'%length)
    cum_sum=pnl.cumsum()
    cum_sum.to_csv(r'c:\industry_change\cumsum_%d.csv'%length)
    informationRatio=avg/std
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.plot(cum_sum)
    ax.set_xticks([0,242,484,725,967,1213,1475,1699,1934,2186,2424,2669,2913])
    ax.set_xticklabels(['2004','2005','2006','2007','2008','20009','2010','2011','2012','2013','2014','2015','2016'],rotation=30,fontsize='small')
    if time_model==-1:
        ax.set_title('before,length=%d,informationRatio=%f'%(length,informationRatio))
        fig.savefig(r'C:\industry_change\fig\before\length=%d.png'%(length))
    if time_model==1:
        ax.set_title('length=%d,informationRatio=%f'%(length,informationRatio))
        fig.savefig(r'C:\industry_change\signal\momentum\length=%d.png'%(length))


for length in [1,2,5,10]:
    pnl=get_pnl(stocks,dates,length)
    draw(pnl,length)
    print length,time.time()-start
    start=time.time()







