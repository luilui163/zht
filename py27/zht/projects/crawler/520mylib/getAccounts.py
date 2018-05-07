#-*-coding: utf-8 -*-
#author:tyhj
#getAccounts.py 2017/7/27 22:14

import requests
from bs4 import BeautifulSoup
import time


session=requests.Session()

url1=r'http://www.520mylib.com/account/login/'


header1={
    'Host':'www.520mylib.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://www.520mylib.com/account/Login'
}

form1={
    'returnUrl':'',
    'UsernameOrEmailAddress':'986340770@qq.com',
    'Password':,
    'CaptchaDetext':'',
    'CaptchaImage':''
}

url2=r'http://www.520mylib.com/db/category/4'

header2={
    'Host':'www.520mylib.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://www.520mylib.com/home/paper'
}
r2=session.get(url2,headers=header2)
soup2=BeautifulSoup(r2.content,'html')
ul=soup2.find('ul',{'class':'quick-actions'})
aa=ul.findAll('a',{'href':True})
items=[(a['href'],a.text) for a in aa]


item=items[0]#TODO
host=u'http://www.520mylib.com'
url3=host+item[0]
r3=session.get(url3,headers=header2)
soup3=BeautifulSoup(r3.content,'html')
ul=soup3.find('ul',{'class':'quick-actions'})
aa=ul.findAll('a',{'href':True})
entrances=[(a['href'],a.text) for a in aa]


entrance=entrances[0] #TODO
url4=host+entrance[0]


header4={
    'Host':'www.520mylib.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'en-US,zh-CN;q=0.8,zh;q=0.5,en;q=0.3',
    'Connection':'keep-alive',
    'Upgrade-Insecure-Requests':'1'
}

r4=session.get(url4,headers=header4)

print r4.content

# url5=host+'db/goExtranceEx?id=43&num=1'
#
# header5={
#     'Host':'www.520mylib.com',
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
#     'Referer':url4
# }
#
# r5=session.get(url5,headers=header5)


# print r5.content
































