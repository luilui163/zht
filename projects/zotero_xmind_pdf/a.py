# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-07-01  22:27
# NAME:zht-base_on_foxit.py

import sys
import os
import re
import csv

from bs4 import BeautifulSoup

xfdf=open(r'e:\a\Stock and Watson- 2002- Macroeconomic Forecasting Using Diffusion Indexes.xfdf','rb').read()


type(xfdf)


xfdf[-1000:]
