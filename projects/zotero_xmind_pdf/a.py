# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-07-01  22:27
# NAME:zht-base_on_foxit.py
import pandas as pd



df=pd.read_csv(r'e:\a\df.csv',index_col=0)


#----- to find the possible titles


test=df[df['is_title']]





#TODO: merge the lines with line_spread equal 0

