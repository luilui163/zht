#-*-coding: utf-8 -*-
#@author:tyhj

import time
import random
import urllib2
from bs4 import BeautifulSoup



url='http://www.chinamoney.com.cn/fe/Channel/18418'
response=urllib2.urlopen(url)
content=response.read()
soup=BeautifulSoup(content)
div=


print content












