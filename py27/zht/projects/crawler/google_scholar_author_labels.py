#-*-coding: utf-8 -*-
#author:tyhj
#google_scholar_author_labels.py 2017.10.18 12:41

import urllib2
from bs4 import BeautifulSoup
import Queue
import time
import pandas as pd

items=Queue.Queue()
items.put(r'https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=label:financial_econometrics')

itemsDetected=[]
itemsFinished=[]

def parse(url):
    content=urllib2.urlopen(url).read()
    soup=BeautifulSoup(content,'lxml')
    a_tags = soup.findAll('a', {'class': 'gsc_oai_one_int'})
    for tag in a_tags:
        href = tag['href']
        newUrl = r'https://scholar.google.com' + href
        if newUrl not in itemsFinished:
            items.put(newUrl)
        if newUrl not in itemsDetected:
            itemsDetected.append(newUrl)
    itemsFinished.append(url)

def run():
    global itemsDetected

    i=0
    while items.qsize()>0:
        url=items.get()
        parse(url)
        print i,len(itemsDetected)
        i+=1
        time.sleep(0.5)

    itemsDetected = sorted(itemsDetected)
    labels = []
    for item in itemsDetected:
        label = item.split(':')[-1]
        labels.append(label)
    df = pd.DataFrame()
    df['label'] = labels
    df['url'] = itemsDetected
    df.to_csv(r'e:\aa\google_scholar_author_labels.csv')












