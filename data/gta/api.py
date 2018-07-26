# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-03-14  21:57
# NAME:zht-dout.py

import os
import pandas as pd
from zht.data.gta.config import SRC


def read_gta(tbname, *args, **kwargs):
    return pd.read_csv(os.path.join(SRC,tbname+'.csv'),*args,**kwargs)

def read_df_from_gta(tbname, varname, indname, colname):
    table=read_gta(tbname)
    df=pd.pivot_table(table,varname,indname,colname)
    return df

