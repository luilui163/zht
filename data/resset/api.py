# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-03-20  21:32
# NAME:zht-api.py

import pandas as pd
import os

from zht.data.resset.config import SRC

def read_resset(fn):
    df=pd.read_csv(os.path.join(SRC, fn + '.csv'))
    return df



