#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd
import datetime
pd.Timestamp(datetime.datetime(2012,5,1,4,5,1))

df=pd.read_csv('data1.csv',index_col=0)

date=df.index.values
time=df['time'].values

year=[int(str(d)[:4]) for d in date]
month=[int(str(d)[4:6]) for d in date]
day=[int(str(d)[6:]) for d in date]
hour=[int(str(t)[:-4]) for t in time]
minute=[int(str(t)[-4:-2]) for t in time]
second=[int(str(t)[-2:]) for t in time]

index=[]
for i in range(len(year)):
    index.append(pd.Timestamp(year[i],month[i],day[i],hour[i],minute[i],second[i]))
    print index[-1]

df.index=index



test=df[df.code=='A1']

# test['price'][test['direction']=='sell'].plot()
test['price'][test['direction']=='buy'].plot()
buy=test[test['direction']=='buy']
sell=test[test['direction']=='sell']
buy['price'].plot()
sell['price'].plot()










