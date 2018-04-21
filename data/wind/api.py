# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-03-20  19:55
# NAME:zht-parse_src.py

import pandas as pd
import os

from zht.data.wind.config import SRC
from zht.utils.dateu import freq_end



def read_wind(fn, freq):
    df = pd.read_csv(os.path.join(SRC, fn + '.csv'),
                     index_col=0, skipfooter=3)
    df.index=freq_end(df.index, freq)
    return df



