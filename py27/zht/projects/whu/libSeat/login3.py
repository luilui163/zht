#-*-coding: utf-8 -*-
#@author:tyhj



#using firefox explore to analyse the html
import requests
import cookielib
import urllib2
from pytesseract import pytesseract
from PIL import Image
import cStringIO
from captchaRecognization import detectCaptcha



urlMain=r'http://seat.lib.whu.edu.cn/login?targetUri=/'

session=requests.session()
r1=session.get(urlMain)

urlCaptcha=r'http://seat.lib.whu.edu.cn/simpleCaptcha/captcha'

cookies={r1.cookies.items()[0][0]:r1.cookies.items()[0][1]}


# headers={
#     'Host':'seat.lib.whu.edu.cn',
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
#     'Referer':'http://seat.lib.whu.edu.cn/login?targetUri=%2F',
# }

headers={
    'Host':'seat.lib.whu.edu.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept':'*/*',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding':'gzip, deflate',
    'Referer':'http://seat.lib.whu.edu.cn/login?targetUri=%2F',
    'Cookie':'='.join(r1.cookies.items()[0]),
    'Connection':'keep-alive',
    'Cache-Control':'max-age=0'
}
# session.cookies=cookielib.LWPCookieJar()
r2=session.get(urlCaptcha,headers=headers,cookies=cookies)
content2=r2.content

captcha=detectCaptcha(content2)

urlSignin=r'http://seat.lib.whu.edu.cn/'

headers = {
    'Host':'seat.lib.whu.edu.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Cookie':'='.join(r1.cookies.items()[0])
}
postdata={
    'username':'2016201050151',
    'password':'100779',
    'captcha':captcha
}

r3=session.post(urlSignin,data=postdata,headers=headers,cookies=cookies)


content=r3.text
# print content
content=content.encode('utf-8')
with open('content.html','w') as f:
    f.write(content)


# content1=response1.content.encode('utf-8')
# with open('content1.html','w') as f:
#     f.write(content1)

print r1.cookies
print r2.cookies
print r3.cookies
print headers
print len(content)#8806

print cookies