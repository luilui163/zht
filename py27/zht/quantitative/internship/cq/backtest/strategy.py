# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 10:26:07 2016

@author: hp
"""

import pandas as pd
import numpy as np
import csv
import os
import backtest
import sid
import matplotlib.pyplot as plt

return_df=pd.read_csv(R'c:\cq\return_df.csv',index_col=0)
return_df_dates=list(return_df.index)
return_df_stocks=list(return_df.columns)


###########################################################################################
lines=open('data.csv').read().split('\n')[:-1]
colnames=lines[0].split(',')
data=[l.split(',')for l in lines[1:]]
df=pd.DataFrame(data,columns=colnames)

variable={}
for j in range(len(data[0])):
    variable[colnames[j]]=[data[i][j] for i in range(len(data))]

discrete_variable=['industry','category']
continuous_variable=['stock_number','holding_ratio','continuous_variable']
##########################################################################################

def process_discrete_variables():
    category={}
    for v in range(len(discrete_variable)):
        test=variable[discrete_variable[v]]
        numbers={}
        for t in test:
            numbers.setdefault(t,0)
            numbers[t]+=1
        aa=[(key,str(numbers[key])) for key in numbers]
        aa.sort(key=lambda x:int(x[1]),reverse=True)
        category[discrete_variable[v]]=aa

    if not os.path.isdir('category'):
        os.makedirs('category')

    for item in category:
        with open(os.path.join('category',item+'.txt'),'w') as f:
            for m in category[item]:
                f.write('%s\t%s\n'%m)
    
    return category

def process_continuous_variables(slice_number=5):
    #slice_number means how many parts to separate the continuous variable
    continuous={}
    for cv in continuous_variable:
        continuous[cv]=[]
        items=variable[cv]
        for item in items:
            try:
                continuous[cv].append(float(item))
            except:
                print '%s is not valid in %s'%(item,cv)
                pass
            
    quantile_values={}

    for c in continuous:
        aa=continuous[c]
        aa.sort()
        values=[aa[0]]
        values+=[aa[int(len(aa)*i/slice_number)] for i in range(1,slice_number)]
        values+=[aa[-1]]
        quantile_values[c]=values

    if not os.path.isdir('continuous'):
        os.makedirs('continuous')
    
    for item in quantile_values:
        with open(os.path.join('continuous',item+'.txt'),'w') as f:
            for m in quantile_values[item]:
                f.write('%s\n'%str(m))

    return quantile_values




#test category variables

def discrete_variable_to_pnls(discrete_variable):
    alphas={}
    for item in discrete_variable_dict[discrete_variable][:5]:
        #compare the max 5 category
        name=item[0]
        alphas.setdefault(name,[])
        values=df[discrete_variable]
        for i in range(len(values)):
            if values[i]==name:
                stock=sid.normalize_sid(df['sid'][i])
                start_date=backtest.shift_date(df['announcement_date'][i])
                end_date=backtest.shift_date(start_date)
                alphas[name].append((stock,start_date,end_date,1))
    
    name_dict={}
    for n,alpha in enumerate(alphas):
        name_dict[alpha]=str(n)
    
    pnls={}
    for alpha in alphas:
        pnls[name_dict[alpha]]=backtest.position_to_pnl(backtest.alpha_to_position(alphas[alpha]))
    
    return pnls,name_dict





def plot2(variable,pnls,name_dict):
    pnl_df=pd.DataFrame(pnls)
    
    e=0
    for i in range(len(pnl_df)):
        flag=0
        for j in range(len(pnl_df.columns)):
            if pd.notnull(pnl_df.iat[i,j]):
                flag=1
                break
        if flag:
            e=i
            break
    pnl_df=pnl_df.iloc[e:]
    count=pnl_df[pd.notnull(pnl_df)].count()
    positive=pnl_df[pnl_df>0].count()
    win_rate=positive/count
    
    
    pnl_df.iloc[0]=0
    std=pnl_df.std()
    avg=pnl_df.mean()
    information_ratio=avg/std
    pnl_df=pnl_df.fillna(0)
    cum_sum=pnl_df.cumsum()
    fig,ax=plt.subplots(1,1,figsize=(12,8))
    #fig=plt.figure()
    #ax=fig.add_subplot(1,1,1)
    ax.plot(cum_sum)
    
    year=[y/10000 for y in list(cum_sum.index)]
    xticks=[]
    xticklabels=[]
    for i in range(1,len(year)):
        if year[i]>year[i-1]:
            xticks.append(i)
            xticklabels.append(str(year[i]))
            
    if len(xticks)<3:
        year=[y/100 for y in list(cum_sum.index)]
        xticks=[]
        xticklabels=[]
        for i in range(1,len(year)):
            if year[i]>year[i-1]:
                xticks.append(i)
                xticklabels.append(str(year[i]))
            
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels,rotation=90,fontsize='small')
    #ax.set_title('IR=%f'%information_ratio)
    
    plt.legend(tuple(pnl_df.columns),loc='upper center')
    plt.title(variable)
    figname=r'category\%s.png'%variable
    fig.savefig(figname)
    
    legend_name_map=[(value,key) for key,value in name_dict.iteritems()]
    description=[(a[0],a[1],str(information_ratio[a[0]]),str(win_rate[int(a[0])])) for a in legend_name_map]
    description.sort(key=lambda x:float(x[2]))
    with open(r'category\%s_description.txt'%variable,'w') as f:
        for d in description:
            f.write('\t'.join(list(d))+'\n')



discrete_variable_dict=process_discrete_variables()
continuous_variable_dict=process_continuous_variables(slice_number=5)

#for dv in discrete_variable_dict:
#    pnls,name_dict=discrete_variable_to_pnls(dv)
#    plot2(dv,pnls,name_dict)
#    print '%s has been plotted'%dv



cv=continuous_variable[0]
values=list(df[cv])



alphas={}
slice_mark=continuous_variable_dict[cv]
interval_label={}
for i in range(len(slice_mark)-1):
    interval_label[str(i)]='(%s,%s]'%(str(slice_mark[i]),str(slice_mark[i+1]))

def extract_data(n):
    def interval(data):
        try:
            return slice_mark[n]<float(data)<=slice_mark[n+1]
        except:
            return False
    return interval

valid_inds=[]
for i in range(len(slice_mark)-1):
    valid_ind=[]
    for v in range(len(values)):
        if extract_data(i)(values[v]):
            valid_ind.append(v)
    valid_inds.append(valid_ind)

announcement_dates=df['announcement_date']
stocks=df['sid']

alphas={}
for i in range(len(valid_inds)):
    alpha=[]
    for vi in valid_inds[i]:
        stock=sid.normalize_sid(stocks[vi])
        start_date=backtest.shift_date(announcement_dates[vi])
        end_date=backtest.shift_date(start_date)
        
        alpha.append((stock,start_date,end_date,1))
    alphas[str(i)]=alpha
    print i

pnls={}
for alpha in alphas:
    pnls[alpha]=backtest.position_to_pnl(backtest.alpha_to_position(alphas[alpha]))
    print alpha
    
name_dict={interval_label[key]:key for key in interval_label}
plot2(cv,pnls,name_dict)



#
#for item in discrete_variables[discrete_variable][:5]:
#    #compare the max 5 category
#    name=item[0]
#    alphas.setdefault(name,[])
#    values=df[discrete_variable]
#    for i in range(len(values)):
#        if values[i]==name:
#            stock=sid.normalize_sid(df['sid'][i])
#            start_date=backtest.shift_date(df['announcement_date'][i])
#            end_date=backtest.shift_date(start_date)
#            alphas[name].append((stock,start_date,end_date,1))
#
#name_dict={}
#for n,alpha in enumerate(alphas):
#    name_dict[alpha]=str(n)
#
#pnls={}
#for alpha in alphas:
#    pnls[name_dict[alpha]]=backtest.position_to_pnl(backtest.alpha_to_position(alphas[alpha]))
#
#


'''
1,Input data form:csv with title
    sid|date1|date2|.....variable1|variable2...|returns
    

to begin with ,we need to preprocess the input data,
deal with '--','NaN' and so on
    
2,Variable:

the description for variable:
format:(name,property,values)
for property:
    if the property is continuous_variable,the values will be 
    splitted into 5 part according the values of the variable
    
    if the property is catogery_variable:
        for chinese character,there should be a dict to map the chinese 
        character to c_number

        
the value for ticker will be changed to the standard above


first our function will get a report about all the variables,
the content in the report will contain follow items:
variable name
property:continuous_variable or category_variable
    continuous_variable will get 5 class,and some describe statistics
    category_variable will get all the category

max
min
median
quantile
mode
std
cov


3,compare:

output:
fig
txt file to explain the legend and sorted IR, win rate
in format:
mark    name    IR    win_rate
     
'''