# -*-coding: utf-8 -*-
# author:zhang haitao
import os
from bs4 import BeautifulSoup as bs
import requests


url=r'https://pandas.pydata.org/pandas-docs/stable/api.html#'
content=requests.get(url).content.decode('utf-8')
soup=bs(content,'html.parser').findAll('div',{'class':'section'})[0]
html=str(soup)
tags=bs(html,'html.parser').findAll('a',{'class':'headerlink'})
with open('pandas_menu.html','w',encoding='utf-8') as f:
    for tag in tags:
        html=html.replace(str(tag),'')
    html=html.replace('generated',r'https://pandas.pydata.org/pandas-docs/stable/generated')
    f.write(html)
