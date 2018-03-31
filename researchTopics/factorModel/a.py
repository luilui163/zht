# -*-coding: utf-8 -*-
# author:tyhj
# anlalyseAlphat.py 2017/9/30 16:50
import pandas as pd
import numpy as np

import os

from params import *
from tools import *


def getAlphatSummary():
    fns = os.listdir(alphatp)
    dfs = [pd.read_csv(os.path.join(alphatp, fn), index_col=0) for fn in fns]
    df = pd.concat(dfs, axis=1)

    for i, col in enumerate(df.columns):
        df.loc['gt2', col] = df[df[col] > 2.0].shape[0]
        df.loc['lt-2', col] = df[df[col] < -2.0].shape[0]
        df.loc['sum', col] = df.loc['gt2', col] + df.loc['lt-2', col]
        print i

    sind = ['gt2', 'lt-2', 'sum']
    newIndex = sind + [ind for ind in df.index if ind not in sind]

    df = df.reindex(index=newIndex)
    df = df.sort_values('sum', axis=1)
    # corr=df.corr()#TODO: delete similar models

    df = df.T
    df.to_csv(os.path.join(eaoatmp, 'alphatSummary.csv'))


def getalphatFinal():
    summary = pd.read_csv(os.path.join(eaoatmp, 'alphatSummary.csv'), index_col=0)
    summary = summary.dropna(how='all', axis=1)

    cols = ['gt2', 'lt-2', 'sum']
    newCols = [col for col in summary.columns if col not in cols]
    alphat = summary[newCols]

    # get valid indicators
    corr = alphat.T.corr()
    corr.to_csv(os.path.join(eaoatmp, 'corrIndicators.csv'))
    np.fill_diagonal(corr.values, 0)
    invalidIndicators = []
    validIndicators = []
    for i in range(corr.shape[1]):
        target = corr.columns[i]
        models = corr[corr[target] == 1].index.tolist()
        if len(models) == 0:
            validIndicators.append(target)
        else:
            for model in models:
                if model not in invalidIndicators + validIndicators:
                    invalidIndicators.append(model)
            if target not in invalidIndicators:
                validIndicators.append(target)
        print i

    newCorr = corr.loc[validModels, validModels]
    np.fill_diagonal(newCorr.values, 1)
    newCorr.to_csv(os.path.join(eaoatmp, 'corrModelsNew.csv'))

    # get valid models
    alphat = alphat.T
    corr = alphat.T.corr()
    corr.to_csv(os.path.join(eaoatmp, 'corrModels.csv'))

    np.fill_diagonal(corr.values, 0)

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

    alphatFinal = summary.loc[validModels, validIndicators]
    # alphatFinal.to_csv(os.path.join(eaoatmp,'alphatFinal.csv'))

# TODO:analyse grs and grsp as methods in mispricing factor





