#-*-coding: utf-8 -*-
#author:tyhj
#baseData.py 2017/7/27 11:17
import pandas as pd
import os


dirpath=r'E:\GTA\csv'


fn='FS_Combas'

df=pd.read_csv(os.path.join(dirpath,fn+'.csv'),index_col=0)


print df.head()














