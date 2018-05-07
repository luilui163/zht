#-*-coding: utf-8 -*-
#author:tyhj
#crawler_sxu.py 2017/7/23 19:37

import requests
from bs4 import BeautifulSoup


session=requests.Session()

url1=r'http://portal.sxu.edu.cn:2048/login?url=http://www.gtarsc.com/'
header1={
    'Host':'portal.sxu.edu.cn:2048',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://www.520mylib.com/db/goExtranceEx?id=891&num=1'
}
form={
    'username':,
    'password':,
    'user':,
    'pass':
}
r1=session.post(url1,data=form,headers=header1)

with open(r'c1.html','w') as f:
    f.write(r1.content)


url2=r'http://portal.sxu.edu.cn:2119/Login/Login'

header2={
    'Host':'portal.sxu.edu.cn:2119',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://portal.sxu.edu.cn:2119/?autoLogin=False'
}

form={
    'UserName':,
    'Password':
}
r2=session.post(url2,data=form,headers=header2)

print r2.content

with open('c2.html','w') as f:
    f.write(r2.content)


url3=r'http://portal.sxu.edu.cn:2119/Home/Index'

header3={
    'Host':'portal.sxu.edu.cn:2119',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://portal.sxu.edu.cn:2119/?autoLogin=False',
}

r3=session.get(url3,headers=header3)

with open('c3.html','w') as f:
    f.write(r3.content)
print r3.content

soup=BeautifulSoup(r3.content,'html')

a=soup.find('input',{'type':'hidden','id':'hdUser'})
value=a['value']
print value


url4=r'http://cn.gtadata.com/Login/Index?versionswitch=%s&control=Home/Index'%value

header4={
    'Host':'cn.gtadata.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://portal.sxu.edu.cn:2119/Home/Index'
}





r4=session.get(url4,headers=header4)
# with open('c4.html','w') as f:
#     f.write(r4.content)
#
# print r4.content
soup=BeautifulSoup(r4.content)
dls=soup.findAll('dl',{'class':'subscriber-list'})
items=[]
for dl in dls:
    category=dl.dt.a.string
    for dd in dl.findAll('dd'):
        items.append([category,dd.a.string,dd.a['href']])





item=items[0]
url5='http://cn.gtadata.com'+item[-1][2:]
header5={
    'Host':'cn.gtadata.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://cn.gtadata.com/Home'
}

r5=session.get(url5,headers=header5)

print r5.content



