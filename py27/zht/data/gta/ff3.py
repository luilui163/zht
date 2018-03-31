#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import statsmodels.api as sm
from zht.data.gta import gtaApi


def regress3f():
    # Fama French 1993 table 3
    eret=gtaApi.getEret()
    rm=gtaApi.getRm()
    rf=gtaApi.getRf()
    factor=gtaApi.getSMBandHML()

    coef = pd.DataFrame(columns=['const', 'smb', 'hml', 'rp'])
    t = pd.DataFrame(columns=['const', 'smb', 'hml', 'rp'])
    r2 = pd.Series()

    errorDfs = []

    for groupId in eret.columns:
        tmpdf = pd.DataFrame()
        tmpdf['eret'] = eret[groupId]
        tmpdf['smb'] = factor['smb']
        tmpdf['hml'] = factor['hml']
        tmpdf['rp'] = rm['rm'] - rf['rf']

        X = tmpdf[['smb', 'hml', 'rp']].as_matrix()
        X = sm.add_constant(X)x
        y = tmpdf['eret'].values

        model = sm.OLS(y, X)
        results = model.fit()

        coef.loc[groupId] = results.params
        t.loc[groupId] = results.tvalues
        r2[groupId] = results.rsquared_adj

        err = pd.DataFrame(results.resid, index=tmpdf.index, columns=[groupId])
        errorDfs.append(err)
    errorDf = pd.concat(errorDfs, axis=1)

    coef.to_csv(r'D:\quantDb\researchTopics\fama\regression\coef.csv')
    t.to_csv((r'D:\quantDb\researchTopics\fama\regression\t.csv'))
    r2.to_csv((r'D:\quantDb\researchTopics\fama\regression\r2.csv'))
    errorDf.to_csv(r'D:\quantDb\researchTopics\fama\regression\error.csv')



#TODO:delete the financial stocks
#TODO:and analyse the financial stocks independently




