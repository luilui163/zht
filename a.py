# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-08-27  21:42
# NAME:FT_hp-a.py

import os
import pandas as pd
# import copy

import numpy as np


from memory_profiler import profile
#
# fp=open(os.path.join(DIR_TMP,'memory_debug.log'),'a')
fp=open('memory_debug.log','a')


# names=os.listdir(r'G:\FT_Users\HTZhang\FT\data_mining\result')
# name = names[0]



# @profile(precision=4)
def tmp_func():
    # global name
    # name='2-ratio_history_compound_growth-tot_bal_netcash_inc-tot_profit'
    # df = pd.read_pickle(os.path.join(r'G:\FT_Users\HTZhang\FT\data_mining\result', name, 'monthly.pkl'))

    pd.DataFrame()
    pd.DataFrame()

    # np.array((3,4))
    # print(df.info())
    # df = df.groupby('month_end').filter(
    #     lambda s: len(s) > 300)  # trick: at least 300 samples in each month
    # df[name] = df[name].groupby('month_end').apply(outlier)
    # df[name] = df[name].groupby('month_end').apply(z_score)
    # df = df.iloc[:, 0].unstack().T
    # df.to_pickle(name+'.pkl')
    # print(name)
    return




@profile(precision=4,stream=fp)
def run():
    # print(names.__sizeof__()/(1024*1024))
    # name='2-ratio_history_compound_growth-tot_bal_netcash_inc-tot_profit'
    # name=names[0]
    # name=copy.copy(names[0])
    # del names
    # print(locals())
    tmp_func()



    # print(locals())

    # for nm in names[:2]:
    #     tmp_func(nm)

if __name__ == '__main__':
    run()
    # run()
