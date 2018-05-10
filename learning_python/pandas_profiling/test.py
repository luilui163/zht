# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-05-10  10:15
# NAME:zht-test.py

import pandas as pd
import pandas_profiling as pp
import numpy as np

if __name__ == '__main__':

    path=r'e:\a\Meteorite_Landings.csv'

    df=pd.read_csv(path,parse_dates=['year'],encoding='utf-8')
    df['year']=pd.to_datetime(df['year'],errors='coerce')
    df['source']='NASA'
    df['bolean']=np.random.choice([True,False],df.shape[0])
    df['mixed']=np.random.choice([1,'A'],df.shape[0])
    df['reclat_city']=df['reclat']+np.random.normal(scale=5,size=(len(df)))

    duplicates_to_add=pd.DataFrame(df.iloc[0:10])
    duplicates_to_add[u'name']=duplicates_to_add[u'name']+'copy'
    df=df.append(duplicates_to_add,ignore_index=True)

    result=pp.ProfileReport(df)
    result.to_file(r'e:\a\result.html')



