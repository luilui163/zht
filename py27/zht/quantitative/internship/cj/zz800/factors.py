#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import numpy as np
import tool
import os
import data_preprocess
import shutil

#把subfactor 等权重相加
def combine_subfactors(df,subfactors,factorname):
    subfactors=list(subfactors)
    if len(subfactors)>1:
        #多个subfactor合并
        tmp_df=df[subfactors]
        weighted_avg=pd.DataFrame(tmp_df.mean(axis=1))
        weighted_avg.columns=[factorname]
        return weighted_avg
    else:
        #只有一个subfactor
        return df[subfactors]

#因子标准化
def standardize(df,factor):
    return tool.standardize(df,factor)

#得到最终的流动性风险暴露值
def get_liquidity_factor():
    if os.path.isdir(r'C:\data\zz800\data_processed\liquidity'):
        shutil.rmtree(r'C:\data\zz800\data_processed\liquidity')
    os.makedirs(r'C:\data\zz800\data_processed\liquidity')

    path = r'C:\data\zz800\liquidity'
    directorys=os.listdir(path)
    paths=[os.path.join(path,d) for d in directorys]
    # 可能不同文件夹下包含的文件名不对应
    intersection_filenames=data_preprocess.get_intersection_filenames(paths)
    for filename in intersection_filenames:
        combined_discriptors=pd.DataFrame()
        for directory in directorys:
            discriptor=pd.read_csv(os.path.join(path,directory,filename),index_col=0)
            discriptor.columns=[directory]#把列名中的中文变为英文
            #处理极值
            discriptor=tool.handle_outliers(discriptor,discriptor.columns[0])
            #标准化
            discriptor=tool.standardize(discriptor,discriptor.columns[0])
            combined_discriptors[directory]=discriptor[directory]
        #合并subfactors
        combined_discriptors=combine_subfactors(combined_discriptors,combined_discriptors.columns,'turnover')
        #标准化时候，市值加权得到中心值
        combined_discriptors = tool.standardize_by_cap_weight(combined_discriptors, combined_discriptors.columns[0])
        combined_discriptors=standardize(combined_discriptors,'turnover')
        combined_discriptors.to_csv(r'C:\data\zz800\data_processed\liquidity\%s'%filename)
        print filename


if __name__=='__main__':
    get_liquidity_factor()

























