#-*-coding: utf-8 -*-
#@author:tyhj

import tushare as ts
import os

df=ts.get_stock_basics()
codes2=df.index.tolist()

files=os.listdir(r'C:\zht\OneDrive\script\rf\stock_monitor\sina')
codes1=[f[:6] for f in files]
codes=[c for c in codes2 if c not in codes1]
codes=sorted(codes)
dir=r'C:\zht\OneDrive\script\rf\stock_monitor\sina'



f=open('codes_abnormal.txt','w')
for code in codes:
    filename=dir+r'\%s.csv'%code
    df = ts.get_h_data(code, start='2005-01-01', end='2016-12-04',autype='qfq')  # forward adjusted price
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=None)
    else:
        try:
            df.to_csv(filename)
        except:
            f.write(code+'\n')
    print code

f.close()









