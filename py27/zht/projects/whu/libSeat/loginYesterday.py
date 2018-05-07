#-*-coding: utf-8 -*-
#@author:tyhj



#using firefox explore to analyse the html
import requests
import cookielib
import urllib2

url=r'http://seat.lib.whu.edu.cn/'

headers = {
    'Host':'seat.lib.whu.edu.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Cookie':'JSESSIONID=8E3E8290C971CDCB22317EAFFA024FCF'#TODO
}
postdata={

    'captcha':'vi7e4'#TODO
}

session=requests.session()
session.cookies = cookielib.LWPCookieJar()#TODO:neccessary?
response=session.post(url,data=postdata,headers=headers)


content=response.text
print content
content=content.encode('utf-8')
with open('content.html','w') as f:
    f.write(content)



url1=r'http://seat.lib.whu.edu.cn/freeBook/ajaxSearch'

response1=session.post(url1,headers=headers)

# content1=response1.content.encode('utf-8')
# with open('content1.html','w') as f:
#     f.write(content1)

print len(response1.content)




