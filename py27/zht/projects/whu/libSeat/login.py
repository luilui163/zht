#-*-coding: utf-8 -*-
#@author:tyhj



#using firefox explore to analyse the html
import requests
import cookielib
import urllib2
from pytesseract import pytesseract

from captchaRecognization import getCaptcha

# url=r'http://seat.lib.whu.edu.cn/'


url=r'http://seat.lib.whu.edu.cn/login?username=%s'%username


#https://www.zhihu.com/question/19786827
session=requests.session()

r1=requests.get(url)
cookie=r1.cookies.values()[0]

headers={
    'Host': 'seat.lib.whu.edu.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':url,
    'Cookie':cookie
}
urlCaptcha=r'http://seat.lib.whu.edu.cn/simpleCaptcha/captcha'
r2=requests.get(urlCaptcha,headers=headers,cookies=r1.cookies)



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



urlLogin=r'http://seat.lib.whu.edu.cn/auth/signIn'
headers = {
    'Host':'seat.lib.whu.edu.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Cookie':'85AD243F43E9A20337C4CADD3B0C5B7A'#TODO
}
postdata={
    'username':username,
    'password':password,
    'captcha':'3ic3k'#TODO
}

session=requests.session()
session.cookies = cookielib.LWPCookieJar()
response=session.post(urlLogin,data=postdata,headers=headers)


content=response.text
print content
content=content.encode('utf-8')
with open('content.html','w') as f:
    f.write(content)



# url1=r'http://seat.lib.whu.edu.cn/freeBook/ajaxSearch'
#
# response1=session.post(url1,headers=headers)
# content1=response1.text
# content1=content1.encode('utf-8')
# with open('content1.html','w') as f:
#     f.write(content1)





