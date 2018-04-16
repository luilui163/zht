# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-04-15  08:50
# NAME:zht-rename_caj.py

import os
from bs4 import BeautifulSoup




import xml.etree.ElementTree as ET
import pandas as pd

class XML2DataFrame:

    def __init__(self, xml_data):
        self.root = ET.XML(xml_data)

    def parse_root(self, root):
        return [self.parse_element(child) for child in iter(root)]

    def parse_element(self, element, parsed=None):
        if parsed is None:
            parsed = dict()
        for key in element.keys():
            parsed[key] = element.attrib.get(key)
        if element.text:
            parsed[element.tag] = element.text
        for child in list(element):
            self.parse_element(child, parsed)
        return parsed

    def process_data(self):
        structure_data = self.parse_root(self.root)
        return pd.DataFrame(structure_data)

xml_data=open(r'E:\a\items.eln',encoding='utf8').read()


xml2df = XML2DataFrame(xml_data)
df = xml2df.process_data()
df=df.sort_values('PubTime',ascending=False)
df=df.reset_index()
df.to_csv(r'e:\a\df.csv', encoding='gbk')

fns=os.listdir(r'e:\a\papers')
target_authors=['唐文进','宋清华','朱新蓉']

items=[]
for fn in fns:
    if fn[:-4] in df['Title'].tolist():
        ind=df['Title'].tolist().index(fn[:-4])
        authors=df.iloc[ind]['Author'].split(';')
        name=''
        for ta in target_authors:
            if ta in authors:
                name=ta

        year=df.iloc[ind]['Year']

        os.rename(os.path.join(r'e:\a\papers',fn),os.path.join(r'e:\a\papers','{}-{}-{}'.format(name,year,fn)))




