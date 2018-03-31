#-*-coding: utf-8 -*-
#author:tyhj
#anlalyseAlphat.py 2017/9/30 16:50
import pandas as pd
import numpy as np

import os

from params import *
from tools import *

fns = os.listdir(alphatp)
dfs = [pd.read_csv(os.path.join(alphatp, fn), index_col=0) for fn in fns]
df = pd.concat(dfs, axis=1)
df=df.dropna(how='all',axis=1)

#get valid models
corr=df.corr()
corr.to_csv(os.path.join(eaoatmp,'corrModels.csv'))
np.fill_diagonal(corr.values,0)

invalidModels = []
validModels = []
for i in range(corr.shape[1]):
    target = corr.columns[i]
    models = corr[corr[target] == 1].index.tolist()
    if len(models) == 0:
        validModels.append(target)
    else:
        for model in models:
            if model not in invalidModels + validModels:
                invalidModels.append(model)
        if target not in invalidModels:
            validModels.append(target)
    print i

newCorr = corr.loc[validModels, validModels]
np.fill_diagonal(newCorr.values, 1)
newCorr.to_csv(os.path.join(eaoatmp, 'corrModelsNew.csv'))

#get valid indicators
corr=df.T.corr()
corr.to_csv(os.path.join(eaoatmp,'corrIndicators.csv'))
np.fill_diagonal(corr.values, 0)
invalidIndicators = []
validIndicators = []
for i in range(corr.shape[1]):
    target = corr.columns[i]
    indicators = corr[corr[target] == 1].index.tolist()
    if len(indicators) == 0:
        validIndicators.append(target)
    else:
        for model in indicators:
            if model not in invalidIndicators + validIndicators:
                invalidIndicators.append(model)
        if target not in invalidIndicators:
            validIndicators.append(target)
    print i

newCorr = corr.loc[validIndicators, validIndicators]
np.fill_diagonal(newCorr.values, 1)
newCorr.to_csv(os.path.join(eaoatmp, 'corrIndicatorsNew.csv'))


#summarize the alphat
dfNew=df.loc[validModels,validIndicators]
dfNew=dfNew.T
for i, col in enumerate(dfNew.columns):
    dfNew.loc['gt2', col] = dfNew[dfNew[col] > 2.0].shape[0]
    dfNew.loc['lt-2', col] = dfNew[dfNew[col] < -2.0].shape[0]
    dfNew.loc['sum', col] = dfNew.loc['gt2', col] + dfNew.loc['lt-2', col]
    print i

sind = ['gt2', 'lt-2', 'sum']
newIndex = sind + [ind for ind in dfNew.index if ind not in sind]

dfNew = dfNew.reindex(index=newIndex)
dfNew = dfNew.sort_values('sum', axis=1)
# corr=dfNew.corr()#TODO: delete similar indicators

dfNew = dfNew.T
dfNew.to_csv(os.path.join(eaoatmp, 'alphatSummary.csv'))

print 'finished'