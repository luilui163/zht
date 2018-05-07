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
from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np
from datetime import datetime




session=requests.session()
##------------------------------------------------------------------------------------------------------
#get the cookies
urlMain=r'http://seat.lib.whu.edu.cn/login?targetUri=/'
headers1={
    'Host': 'seat.lib.whu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
}

session.get(urlMain)
r1=session.get(urlMain)

##-------------------------------------------------------------------------------------------------------
#detect captcha
urlCaptcha=r'http://seat.lib.whu.edu.cn/simpleCaptcha/captcha'
headers2={
    'Host':'seat.lib.whu.edu.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://seat.lib.whu.edu.cn/login?targetUri=%2F'
}
r2=session.get(urlCaptcha,headers=headers2)
captcha=detectCaptcha(r2.content)
captcha=captcha.replace(' ','')

##-------------------------------------------------------------------------------------------------
#login in
urlSignin=r'http://seat.lib.whu.edu.cn/auth/signIn'
headers3 = {
    'Host':'seat.lib.whu.edu.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
}
postdata3={
    'username':username,
    'password':password,
    'captcha':captcha
}

r3=session.post(urlSignin,data=postdata3,headers=headers3)

if len(r3.content)>100000:
    print 'the captcha is:%s'%captcha
    print 'login in successfully!'

##------------------------------------------------------------------------------------------------
#get all the seat ID
def getIds():
    headers4 = {
        'Host':'seat.lib.whu.edu.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Referer':'http://seat.lib.whu.edu.cn/',
    }

    items=[]
    offset=0
    while True:
        urlSeatList=r'http://seat.lib.whu.edu.cn/freeBook/ajaxSearch?onDate=2017-07-07&building=1&room=&hour=null&power=null&startMin=null&endMin=null&offset=%s'%offset
        r4=session.get(urlSeatList,headers=headers4)
        content=r4.content
        seatStr=json.loads(content)['seatStr']
        soup=BeautifulSoup(seatStr,'lxml')
        lis=soup.find_all('li')
        if lis:
            for li in lis:
                id=li['id']
                cla=li['class']
                title=li['title']
                num=li.dt.text
                area=li.dd.text
                items.append((id,cla,title,num,area))
            offset += 1
            print offset
        else:
            break

    dfId=pd.DataFrame(items,columns=['id','class','title','seatNumber','area'])
    print dfId.head()
    # df.to_csv('id.csv',encoding='gbk')

#---------------------------------------------------------------------------------
#get seat info

date=datetime.today()
now=datetime.now()
hour=now.hour
minute=now.minute

point1=datetime(now.year,now.month,now.day,21,30)
point2=datetime(now.year,now.month,now.day,22,30)
if now>=point2:
    #book for the next day
    date+=datetime.timedelta(days=1)
elif now>=point1:
    print 'The time is %s.\nIt is too late for today and too early for tomorrow'%now.strftime('%Y-%m-%d %H:%M:%S')

urlSeat=r'http://seat.lib.whu.edu.cn/freeBook/ajaxGetTime'
headers5={
    'Host': 'seat.lib.whu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Referer': 'http://seat.lib.whu.edu.cn/'
}

dfId=pd.read_csv('id.csv',index_col=0,encoding='gbk')
ids=[str(s.split('_')[-1]) for s in dfId['id']]


start=datetime(date.year,date.month,date.day,8,0)
end=datetime(date.year,date.month,date.day,21,30)
timeRange=pd.date_range(start=start,end=end,freq='30min')
timeRange=[str(t.strftime('%H:%M')) for t in timeRange]

dfTime=pd.DataFrame(np.nan,index=ids,columns=['now']+timeRange)

for i,id in enumerate(ids):
    postdata5={'id':str(id),'date':date.strftime('%Y-%m-%d')}
    r5=session.post(urlSeat,data=postdata5,headers=headers5)
    content5=r5.content
    soup5=BeautifulSoup(content5,'lxml')
    lis=soup5.find_all('li')
    availableTime=[li.text for li in lis]

    availableTime=[str(a) if len(a)==5 else 'now' for a in availableTime]
    #TODO: if this seat is available for the whole day,book it and exit,and otherwise continue the following process

    dfTime.loc[str(id),availableTime]=1
    print '%s/%s:%s'%(i+1,len(ids),id)

dfTime.to_csv('dfTime.csv')
#----------------------------------------------------------------------------------
#rank the available seats
'''
factors:
continuity
time interval
right now?
break point?
'''
grade=dfTime
grade=grade.dropna(axis=1,how='all')
tmp=grade.fillna(0)
s=tmp.cumprod(axis=1)
grade['grade']=s.sum(axis=1)
# grade=grade.sort_values('grade',ascending=False)
# # grade=grade.dopna(axis=1,how='all')
# grade.to_csv('grade.csv')

prioritySeats=open('prioritySeats.txt').read().split('\n')

grade['priority']=False
grade.loc[prioritySeats,'priority']=True
grade=grade.sort_values(['priority','grade'],ascending=False)
grade.to_csv('grade.csv')

#---------------------------------------------------------------------------
#book seat
urlBook=r'http://seat.lib.whu.edu.cn/selfRes'
headers6={
    'Host': 'seat.lib.whu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Referer': 'http://seat.lib.whu.edu.cn/'
}

mapId={dfId['id'][i][-4:]:(dfId['seatNumber'][i],dfId['area'][i]) for i in range(dfId.shape[0])}

mapTime={t:str(int(t.split(':')[0])*60+int(t.split(':')[1])) for t in grade.columns[1:-2]}

i=0
while True:
    target=grade.ix[i]
    id=target.name
    if target.index[0]=='now':
        start='now'
    else:
        start=mapTime[target.index[0]]
    end=mapTime[target.index[target[-2]-1]]

    postdata6={
        'date':date.strftime('%Y-%m-%d'),
        'seat':id,
        'start':start,
        'end':end,
        'captcha':''
    }

    r6=session.post(urlBook,data=postdata6,headers=headers6)
    print r6.content
    if '凭证号' in r6.content:
        print 'seat [%s] in [%s] has been booked for you'%tuple(mapId[id])
        break
    else:
        i+=1






#1290 for time 21:30













#TODO:1,automatically manage the seats using available accounts;
#TODO:2,monitor the library,such as the summit,time to go lunch,and so on.
#TODO:3,analyse the history to rank the most popular seats

