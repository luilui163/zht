# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-05-21  13:57
# NAME:FT-test_ssh.py
import os
import pandas as pd
dirFactor=r'\\Ft-research\e\Share\Alpha\FYang\factors'
dirHtz=r'\\Ft-research\e\FT_Users\HTZhang'


def read_hdf(name):
    if name.endswith('h5'):
        name=name[:-3]
    return pd.HDFStore(os.path.join(dirFactor,name+'.h5'))


def get_test_data():
    return read_hdf('test_data')

test=get_test_data()
bp=test.get('BP_neu')

unstk=bp.unstack()

print(test.info())