# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-10-05  18:56
# NAME:zht-convert.py
import xmltodict
import os

directory=r'E:\a\xmind2doc\zip'
path=os.path.join(directory,'content.xml')


with open(os.path.join(directory,'content.xml'))  as f:
    # xml=f.read()
    doc=xmltodict.parse(f.read())

import untangle
obj = untangle.parse(os.path.join(directory,'content.xml'))

import xml.etree.ElementTree as et

tree=et.parse(path)

root=tree.getroot()

for child in root:
    print(child.tag,'\n',child.attrib)

for topic in root.iter('topic'):
    print(topic.text)

for topic in root.findall('topic'):
    print(topic.text)

sheet=root[0]
sheet[0].text
sheet[1].tag