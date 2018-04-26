# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-04-25  21:16
# NAME:zht-parse_JEL.py

from urllib.request import urlopen

from utils.parse_xml import XML2DataFrame

url='https://www.aeaweb.org/econlit/classifications.xml'

df=XML2DataFrame(urlopen(url).read()).process_data()

print(df.head())




