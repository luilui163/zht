#-*-coding: utf-8 -*-
#author:tyhj
#dataAPI.py 2017/7/29 11:52

import pandas as pd
import os
from zht.researchTopics.crossSection.params import dp

def get_df(tbname):
    df=pd.read_csv(os.path.join(dp,tbname+'.csv'),index_col=0)
    return df

def save_df(df,tbname):
    df.to_csv(os.path.join(dp,tbname+'.csv'))










