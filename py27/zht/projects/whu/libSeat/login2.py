#-*-coding: utf-8 -*-
#@author:tyhj



#using firefox explore to analyse the html
import requests
import cookielib
import urllib2
from pytesseract import pytesseract

from captchaRecognization import getCaptcha

# url=r'http://seat.lib.whu.edu.cn/'

urlMain=r'http://seat.lib.whu.edu.cn/login?targetUri=/'

session=requests.session()

r1=session.get(urlMain)

text1=r1.text.encode('utf-8')
with open('text1.html','w') as f:
    f.write(text1)




urlCaptcha=r'http://seat.lib.whu.edu.cn/simpleCaptcha/captcha'

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

r2=session.get(urlCaptcha,headers=headers,cookies=r1.cookies)


from PIL import Image
import cStringIO
file = cStringIO.StringIO(r2.content)
im = Image.open(file)
im.show()
im = im.convert('L')
thresh = 125
table = []
for i in range(256):
    if i < thresh:
        table.append(0)
    else:
        table.append(1)
out = im.point(table, '1')
# out.show()
captcha = pytesseract.image_to_string(out)

print captcha




urlSignin=r'http://seat.lib.whu.edu.cn/auth/signIn'

headers={
    'Host':'seat.lib.whu.edu.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding':'gzip, deflate',
    'Content-Type':'application/x-www-form-urlencoded',
    'Content-Length':'52',
    'Referer':'http://seat.lib.whu.edu.cn/login?targetUri=%2F',
    'Cookie':'='.join(r1.cookies.items()[0]),
    'Connection':'keep-alive',
    'Upgrade-insecure-Requests':'1'
}
data={
    'username':username,
    'password':password,
    'captcha':captcha
}

r3=session.get(urlSignin,data=data,headers=headers,cookies=r2.cookies)
text2=r3.text

text2=text2.encoding('utf-8')
with open('text2.html','w') as f:
    f.write(text2)


