# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-08-08  17:31
# NAME:zht-analyze_citavi_sqlite.py


import sqlite3
import sys
import os
import re
import pandas as pd

path1 = r'E:\a\DEMO Food Quality - A Global Challenge (2)\DEMO Food Quality - A Global Challenge (2).sqlite'

import zipfile


def detect_filetype(path):
    import magic
    print(magic.from_file(path))



conn = sqlite3.connect(path1)
c = conn.cursor()

def query(q):
    c.execute(q)
    return c.fetchall()


def analyze_sqlite_structure():
    q = 'select name from sqlite_master where type="table"'
    tbnames = [i[0] for i in query(q)]

    dic = {}
    for tbname in tbnames:
        print(tbname)
        q = 'select * from `{}`'.format(tbname)
        df = pd.DataFrame(query(q), columns=[d[0] for d in c.description])
        dic[tbname] = df

    ss = []
    for k in dic:
        df = dic[k]
        s = pd.Series([1] * df.shape[1], index=df.columns.tolist())
        s.name = k
        ss.append(s)

    comb = pd.concat(ss, axis=1, sort=True)

    comb = comb.sort_values('Annotation')
    comb = comb.T
    comb.to_csv(r'e:\a\comb.csv')


def analyze_encoding(s):
    import chardet
    from encodings.aliases import aliases
    ecs = list(set(aliases.values()))
    for ec in ecs:
        try:
            print('{}\t{}'.format(ec, s.decode(ec)))
        except:
            pass

