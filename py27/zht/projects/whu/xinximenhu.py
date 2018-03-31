#-*-coding: utf-8 -*-
#@author:tyhj
import requests
import cookielib
import urllib2
from pytesseract import pytesseract
from PIL import Image
import cStringIO
from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np
from datetime import datetime


username='2016201050151'
password='100779'


session=requests.session()

url1=r'http://cas.whu.edu.cn/authserver/login?service=http://my.whu.edu.cn/'


header1={
    'Host':'cas.whu.edu.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://my.whu.edu.cn/'
}

r1=session.get(url1,headers=header1)

soup1=BeautifulSoup(r1.content,'lxml')

form=soup1.find_all("form",{'id':'casLoginForm'})[0]

lt=form.find('input',{'name':'lt'})['value']
dllt=form.find('input',{'name':'dllt'})['value']
execution=form.find('input',{'name':'execution'})['value']
_eventId=form.find('input',{'name':'_eventId'})['value']
rmShown=form.find('input',{'name':'rmShown'})['value']

url2=r'http://cas.whu.edu.cn/authserver/login?service=http://my.whu.edu.cn/'

header2={
    'Host': 'cas.whu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://cas.whu.edu.cn/authserver/login?service=http%3A%2F%2Fmy.whu.edu.cn%2F'
}

postdata={'username':username,
          'password':password,
          'lt':lt,
          'dllt':dllt,
          'execution':execution,
          '_eventId':_eventId,
          'rmShown':rmShown
          }

r2=session.post(url2,data=postdata,headers=header2,allow_redirects=False)

#TODO: if there is location ,using allow_redicts

location=r2.headers['location']

url3=location
header3=header2

r3=session.get(url3,headers=header3,allow_redirects=False)





url4=r'http://my.whu.edu.cn/'
header4={
    'Host': 'cas.whu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer': 'http://cas.whu.edu.cn/authserver/login?service=http%3A%2F%2Fmy.whu.edu.cn%2F'
}

r4=session.get(url4,headers=header4)

with open('content4.html','w') as f:
    f.write(r4.content)
print r4.content



#TODO:summarize the tricks of scrawler
