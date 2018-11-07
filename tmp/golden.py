# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-10-24  17:39
# NAME:zht-golden.py
from WindPy import w
import pandas as pd


w.start()

codes='600519.SH,000651.SZ,600276.SH,600066.SH,600518.SH,000538.SZ,000002.SZ,600887.SH,600682.SH,600837.SH,000568.SZ,600703.SH,600867.SH,000895.SZ,000623.SZ,000625.SZ,600705.SH,600201.SH,000768.SZ,000661.SZ'

dfs=[]
for year in range(1996,2018):
    data=w.wss(codes,"div_payoutratio,net_profit_is,mkt_cap_ard,roe,eqy_belongto_parcomsh",f"year={year};unit=1;rptDate={year}1231;rptType=1;tradeDate={year}1231")
    _df=pd.DataFrame(data.Data, columns=codes.split(','), index=data.Fields).T
    dfs.append(_df)
    print(year)

df=pd.concat(dfs, keys=range(1996, 2018))
df.columns=['b', 'E', 'P', 'ROE', 'B']


df.index.names=['year', 'stkcd']

data2=w.wsd(codes, "pct_chg", "1996-01-01", "2017-12-31", "Period=Y;Days=Alldays;PriceAdj=B")
ret=pd.DataFrame(data2.Data,index=data2.Codes,columns=range(1996,2018)).T.stack()

data3=w.wss(codes, "sec_name")
name=pd.Series(data3.Data[0],index=data3.Codes)

df['ret']=ret
df['ret']=df['ret']/100
df['b']=df['b']/100
df['ROE']=df['ROE']/100

df=df.dropna(subset=['ret'])

df=df[df.index.get_level_values('year')>=1997]


df['E/P']=df.groupby('stkcd',as_index=False,group_keys=False).apply(lambda x:x['E']/x['P'].shift(1))
df['B/P']=df.groupby('stkcd',as_index=False,group_keys=False).apply(lambda x:x['B']/x['P'].shift(1))

# df['E/P']=df['E']/df['P']
# df['B/P']=df['B']/df['P']

df=df.groupby('stkcd').mean()

df['gorden1']=(1-df['b'])*df['E/P']+df['b']/df['ROE']
df['gorden2']=df['ROE']*((1-df['b'])*df['B/P']+df['b'])

df['name']=name

df.to_csv(r'e:\a\df.csv',encoding='gbk')
a




