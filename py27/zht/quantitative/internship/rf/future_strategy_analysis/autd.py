#-*-coding: utf-8 -*-
#@author:tyhj
'''
code1:进行基本的描述性统计分析
'''
import pandas as pd
import scipy.stats as stats
import pylab
import numpy as np
import statsmodels.api as sm
from geneview.gwas import qqplot



data=pd.read_csv('autd.csv',index_col=0)#导入数据
data['autd'].plot()#画出价格走势图
returns=data.pct_change()#获得收益率
returns.hist(bins=30)#直方图
returns.plot()#收益率波动图
values=returns['autd'].values

stats.probplot(values,dist='norm',plot=pylab)#qq图
sm.qqplot(values,line='45')
pylab.show()
stats=returns.describe(include='all')
print stats














