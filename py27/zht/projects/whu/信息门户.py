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

username,password=open(r'C:\Python27\zht\whu\account').read().split('\n')
session=requests.session()


url1=r'http://cas.whu.edu.cn/authserver/login?service=http%3A%2F%2Fmy.whu.edu.cn%2F'

header1={
    'Host':'cas.whu.edu.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://my.whu.edu.cn/'
}

r1=session.get(url1,headers=header1)

with open('content1.html','w') as f:
    f.write(r1.content)


r2=r'http://cas.whu.edu.cn/authserver/login?service=http%3A%2F%2Fmy.whu.edu.cn%2F'

header2={
    'Host': 'cas.whu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://cas.whu.edu.cn/authserver/login?service=http%3A%2F%2Fmy.whu.edu.cn%2F'
}









