# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-05-21  17:07
# NAME:FT-dataApi.py

import pymysql
import pandas as pd
import numpy as np
from datetime import timedelta


def read_from_sql(tbname, cols):
    db = pymysql.connect('192.168.1.140', 'ftresearch', 'FTResearch',
                         'ftresearch')
    cur = db.cursor()
    fields = ','.join(cols)
    #TODO: select * from
    #TODO: if there is ....

    query = 'Select ' + fields + ' FROM ' + tbname
    cur.execute(query)
    table = cur.fetchall()
    table = pd.DataFrame(list(table))
    table.columns = cols
    return table

def get_indicator(tbname,indname,freq='M'):
    cols=['stkcd','trd_dt',indname]
    table=read_from_sql(tbname,cols)
    table['trd_dt']=pd.to_datetime(table['trd_dt'])
    table=pd.pivot_table(table,values=indname,columns='stkcd')
    return table


