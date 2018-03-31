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


username='2016201050151'
password='100779'

urlMain=r'http://seat.lib.whu.edu.cn/login?targetUri=/'

session=requests.session()
r1=session.get(urlMain)


urlCaptcha=r'http://seat.lib.whu.edu.cn/simpleCaptcha/captcha'


headers={
    'Host':'seat.lib.whu.edu.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://seat.lib.whu.edu.cn/login?targetUri=%2F',
    'Cookies':'='.join(r1.cookies.items()[0])
}
session=requests.session()
# session.cookies=cookielib.LWPCookieJar()
r2=session.get(urlCaptcha,headers=headers)
content2=r2.content

captcha=detectCaptcha(content2)

urlSignin=r'http://seat.lib.whu.edu.cn/auth/signIn'

headers = {
    'Host':'seat.lib.whu.edu.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Cookie':'='.join(r2.cookies.items()[0])
}
postdata={
    'username':'2016201050151',
    'password':'100779',
    'captcha':captcha
}

r3=session.post(urlSignin,data=postdata,headers=headers)


content=r3.text
# print content
content=content.encode('utf-8')
with open('content.html','w') as f:
    f.write(content)


# content1=response1.content.encode('utf-8')
# with open('content1.html','w') as f:
#     f.write(content1)

print captcha
print r2.cookies
print len(content)#8806


print r1.request.headers
print r2.request.headers
print r3.request.headers