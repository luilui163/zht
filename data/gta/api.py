# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-03-14  21:57
# NAME:zht-dout.py

import os
import pandas as pd
from zht.data.gta.config import SRC


def read_gta(fn):
    return pd.read_csv(os.path.join(SRC,fn+'.csv'))


