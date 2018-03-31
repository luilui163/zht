#-*-coding: utf-8 -*-
#@author:tyhj

import requests
import time

from bs4 import BeautifulSoup

session=requests.Session()


url1=r'http://www1.resset.cn:8080/product/UserLogin'
header1={
    'Host':'www1.resset.cn:8080',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://www1.resset.cn:8080/product/',
    'Connection':'keep-alive'
}
formData={'loginName':'lnu','loginPwd':'lnu'}
r1=session.post(url1,data=formData,headers=header1)

with open('c1.html','w') as f:
    f.write(r1.content)



url2=r'http://www2.resset.cn/product/common/mainFrame.jsp?dbMsgId=4028818a2206ecbc012206edd0d10001'
header2={
    'Host':'www2.resset.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://www2.resset.cn/product/common/main.jsp',
    'Connection':'keep-alive'
}

r2=session.get(url2,headers=header1)

# with open('c2.html','w') as f:
#     f.write(r2.content)


# url3=r'http://www2.resset.cn/product/common/menu.jsp?dbMsgId=4028818a2206ecbc012206edd0d10001'
#
#
# header3={
#     'Host':'www2.resset.cn',
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
#     'Referer':'http://www2.resset.cn/product/common/mainFrame.jsp?dbMsgId=4028818a2206ecbc012206edd0d10001',
#     'Connection':'keep-alive',
#     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#     'Accept-Encoding':'gzip, deflate',
#     'Upgrade-Insecure-Request':'1'
# }
# r3=session.get(url3,headers=header3)
# print r3.content


# url4=r'http://www2.resset.cn/product/db/download/dataSearch.jsp?dlm=101&tableName=DRESSTK_1990_2000&dbMsgId=ff808081432dd4cd014331c9b6b602a8'
# header4={
#     'Host':'www2.resset.cn',
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
#     'Referer':'http://www2.resset.cn/product/common/menu.jsp?dbMsgId=4028818a2206ecbc012206edd0d10001',
# }
#
# r4=session.get(url4,headers=header4)
#
# print r4.content

url4=r'http://www3.resset.cn:8080/product/common/menu.jsp?dbMsgId=4028818a2206ecbc012206edd0d10001'







url=r'http://www3.resset.cn:8080/product/db/download/dataSearch.jsp?dlm=101&tableName=DRESSTK_1990_2000&dbMsgId=ff808081432dd4cd014331c9b6b602a8'





#TODO: use webdriver and phantomjs