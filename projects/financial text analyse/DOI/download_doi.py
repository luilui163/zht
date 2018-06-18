# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-06-18  10:16
# NAME:zht-download_doi.py
import os
import re
import urllib.request
import requests
from habanero import Crossref
import pandas as pd
import json
from bs4 import BeautifulSoup as bs



'''
cursor: denotes the pages
cursor_max: denotes the max number of items
'''
def download_all_json(issn='0893-9454'):
    limit=50
    cr = Crossref()
    for offset in range(0,10000,limit):
        xx=cr.journals(ids=issn,works=True,offset=offset,limit=limit,curosr_max=1000000)['message']['items']
        for i,x in enumerate(xx):
            js=json.dumps(x)
            with open(r'E:\a\test_doi\{}.json'.format(offset+i+1),'w') as f:
                json.dump(js,f)
        print(offset)

def get_all_doi():
    directory=r'E:\a\test_doi'
    fns=os.listdir(directory)
    def _get(fn):
        with open(os.path.join(directory,fn)) as f:
            d=json.loads(json.load(f))
            doi=d['DOI']
        return doi
    dois=[_get(fn) for fn in fns]
    return dois

def download_pdf(doi):
    available_domains=['http://sci-hub.nu/',
                       'https://sci-hub.tw/',
                       'https://sci-hub.nu/',
                       'http://sci-hub.ir/free-paper-download/'
                       ]
    default_domain=available_domains[0]
    url=default_domain+doi
    c=requests.get(url)
    soup=bs(c.content.decode('utf8'),'lxml')
    a=soup.find('a',{'onclick':True})['onclick']
    href=a.split('=')[1][1:]
    urllib.request.urlretrieve(href,r'e:\a\test_pdf\{}.pdf'.format(doi.replace(r'/','_')))

def download_all_pdf():
    dois=get_all_doi()
    for doi in dois[-100:]:
        try:
            download_pdf(doi)
            print(doi)
        except Exception as e:
            print(doi,e)

directory=r'E:\a\test_doi'
fns=os.listdir(directory)
for fn in fns[-100:]:
    x=open(os.path.join(directory,fn))
    js=json.loads(json.load(x))
    doi=js['DOI']
    url=js['URL']

    print(fn,doi,url)



















