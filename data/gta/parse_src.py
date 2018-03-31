# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-03-14  21:47
# NAME:zht-parse_src.py


import os
import pandas as pd
from data.gta.config import txtpath,csvpath

def txt2csv(fns):
    for fn in fns:
        p = os.path.join(txtpath, fn)
        # use python to python engine to parse the data,since there are some files too big.
        try:
            df = pd.read_csv(p, sep='\t', encoding='ISO-8859-1', error_bad_lines=False, skiprows=[1, 2])
        except:
            df = pd.read_csv(p, sep='\t', encoding='ISO-8859-1', error_bad_lines=False, skiprows=[1, 2],
                             engine='python')
        df.to_csv(os.path.join(csvpath, fn[:-4] + '.csv'), encoding='utf-8')
        print(fn)

def update():
    fns=[fn for fn in os.listdir(txtpath) if fn[:-4] not in [x[:-4] for x in os.listdir(csvpath)]]
    txt2csv(fns)

if __name__=='__main__':
    update()












