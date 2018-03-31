# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 15:28:18 2016

@author: hp
"""




def get_result(alpha):
    target_df=pd.DataFrame(np.zeros((len(return_df.index),len(return_df.columns))),index=return_df.index,columns=return_df.columns)
    target_df[target_df==0]=np.nan
    
    col=list(return_df.columns)
    for n,a in enumerate(alpha):
        col_index=col.index(a[0])
        if a[1] and a[2]:
            start_index=return_df_dates.index(int(a[1]))
            end_index=return_df_dates.index(int(a[2]))
            for i in range(start_index,end_index+1):
                target_df.iat[i,col_index]=a[3]
    
    
    return_df_limit=return_df.copy()
    return_df_limit[abs(return_df_limit)>0.095]=0
    r=return_df.mean(axis=1)
    p=return_df_limit*target_df
    pnl=pd.Series([np.nan]*len(target_df),index=return_df.index)
    for i in range(len(target_df)):
        position=target_df.iloc[i]
        long_position=position[position>0].sum()
        short_position=abs(position[position<0].sum())
        if short_position<long_position:
            pnl.values[i]=(p.iloc[i]).sum()/long_position-r.values[i]
        elif short_position>long_position:
            pnl.values[i]=(p.iloc[i]).sum()/short_position+r.values[i]
        elif short_position and long_position:
            pnl.values[i]=(p.iloc[i]).sum()/long_position
    
            
       
    for e,k in enumerate(pnl):
        if pd.notnull(k):
            break
    
    pnl=pnl[e:]
    pnl.values[0]=0
    pnl=pnl.fillna(0)
    std=pnl.std()
    avg=pnl.mean()
    cum_sum=pnl.cumsum()
    information_ratio=avg/std
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.plot(cum_sum)
    
    year=[y/10000 for y in list(cum_sum.index)]
    xticks=[]
    xticklabels=[]
    for i in range(1,len(year)):
        if year[i]>year[i-1]:
            xticks.append(i)
            xticklabels.append(str(year[i]))
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels,rotation=30,fontsize='small')
    ax.set_title('IR=%f'%information_ratio)