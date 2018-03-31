# -*-coding: utf-8 -*-
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-02-10  13:45
# NAME:assetPricing-config.py
import os

DATA_SRC=r'D:\zht\database\quantDb\sourceData\gta\data\csv'

PROJECT_PATH=r'D:\zht\database\quantDb\researchTopics\assetPricingNew'
DATA_PATH=os.path.join(PROJECT_PATH, 'data')
BETA_PATH=os.path.join(PROJECT_PATH,'beta')
SIZE_PATH=os.path.join(PROJECT_PATH,'size')
VALUE_PATH=os.path.join(PROJECT_PATH,'value')
WIND_SRC_PATH=os.path.join(PROJECT_PATH,'wind_src')
WIND_PATH=os.path.join(PROJECT_PATH,'wind')


TMP_PATH=os.path.join(PROJECT_PATH,'tmp')

BETA_NAMES=['1M','3M','6M','12M','24M','1Y','2Y','3Y','5Y']
SIZE_NAMES=['mktCap','size','mktCap_ff','size_ff']
VALUE_NAMES=['bm','logbm']





