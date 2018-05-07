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
headers2={
    'Host':'seat.lib.whu.edu.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://seat.lib.whu.edu.cn/login?targetUri=%2F',
    'Cookies':'='.join(r1.cookies.items()[0])
}
session=requests.session()
r2=session.get(urlCaptcha,headers=headers2)
captcha=detectCaptcha(r2.content)

urlSignin=r'http://seat.lib.whu.edu.cn/auth/signIn'
headers3 = {
    'Host':'seat.lib.whu.edu.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Cookie':'='.join(r2.cookies.items()[0])
}
postdata3={
    'username':username,
    'password':password,
    'captcha':captcha
}

#session=requests.session() #TODO: do not add this line
r3=session.post(urlSignin,data=postdata3,headers=headers3)

'''
#r3.content is str,but r3.text is unicode
with open('content.html','w') as f:
    f.write(r3.content)



urlSeat=r'http://seat.lib.whu.edu.cn/freeBook/ajaxSearch'
headers4 = {
    'Host':'seat.lib.whu.edu.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Referer':'http://seat.lib.whu.edu.cn/',
    'Cookie':'='.join(r3.cookies.items()[0])
}
postdata4={

    'captcha':captcha
}

r4=session.post(urlSignin,data=postdata4,headers=headers4)





'''



print r1.request.headers
print r2.request.headers
print r3.request.headers



print '\n'
print captcha
print r2.cookies
print len(r3.content)#8806

print r3.cookies