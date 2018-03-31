#-*-coding: utf-8 -*-
#author:tyhj
#collectData.py 2017/7/23 0:28
import requests
import cookielib
import urllib2
from pytesseract import pytesseract
from PIL import Image
import cStringIO
from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import os


class BookSeat:
    def __init__(self,username,password,path):
        self.username=username
        self.password=password
        self.path=path
        self.date = datetime.today()
        self.saveData()

    def _getCookies(self):
        #get the cookies
        urlMain = r'http://seat.lib.whu.edu.cn/login?targetUri=/'
        headers1 = {
            'Host': 'seat.lib.whu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
        }

        # self.session.get(urlMain)
        r1 = self.session.get(urlMain)

    def _getCaptcha(self):
        '''detect the captcha'''
        urlCaptcha = r'http://seat.lib.whu.edu.cn/simpleCaptcha/captcha'
        headers2 = {
            'Host': 'seat.lib.whu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Referer': 'http://seat.lib.whu.edu.cn/login?targetUri=%2F'
        }
        r2 = self.session.get(urlCaptcha, headers=headers2)
        captcha = self._detectCaptcha(r2.content)
        captcha = captcha.replace(' ', '')
        return captcha

    def _detectCaptcha(self,content):
        file = cStringIO.StringIO(content)
        im = Image.open(file)
        # im.show()
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
        return captcha

    def login(self):
        self.session = requests.session()
        self._getCookies()
        urlSignin = r'http://seat.lib.whu.edu.cn/auth/signIn'
        headers3 = {
                'Host': 'seat.lib.whu.edu.cn',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
                }
        postdata3 = {
                'username': self.username,
                'password': self.password,
                'captcha': self._getCaptcha()
                }

        r3 = self.session.post(urlSignin, data=postdata3, headers=headers3)

        if len(r3.content) > 10000:
            # print 'the captcha is:%s' % self.captcha
            print 'login in successfully!'
            self.yes=True
        else:
            self.login()

    def getIds(self):
        headers4 = {
            'Host': 'seat.lib.whu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Referer': 'http://seat.lib.whu.edu.cn/',
        }

        items = []
        offset = 0
        while True:
            urlSeatList = r'http://seat.lib.whu.edu.cn/freeBook/ajaxSearch?onDate=%s&building=1&room=&hour=null&power=null&startMin=null&endMin=null&offset=%s' % (self.date.strftime('%Y-%m-%d'),offset)
            r4 = self.session.get(urlSeatList, headers=headers4)
            content = r4.content
            seatStr = json.loads(content)['seatStr']
            soup = BeautifulSoup(seatStr, 'lxml')
            lis = soup.find_all('li')
            if lis:
                for li in lis:
                    id = li['id']
                    cla = li['class']
                    title = li['title']
                    num = li.dt.text
                    area = li.dd.text
                    items.append((id, cla, title, num, area))
                offset += 1
                print offset
            else:
                break

        dfId = pd.DataFrame(items, columns=['id', 'class', 'title', 'seatNumber', 'area'])
        dfId.to_csv(os.path.join(self.path,'current','%s.csv'%datetime.now().strftime('%Y%m%d-%H%M%S')),encoding='gbk')
        self.dfId=dfId

    def getSeatInfo(self):
        #get the informations of all the seats
        now=datetime.now()
        point1 = datetime(now.year, now.month, now.day, 21, 30)
        point2 = datetime(now.year, now.month, now.day, 22, 30)
        if now >= point2:
            # book for the next day
            self.date += timedelta(days=1)
        elif point2>now >= point1:
            print 'The time is %s.\nIt is too late for today and too early for tomorrow' % now.strftime(
                '%Y-%m-%d %H:%M:%S')

        urlSeat = r'http://seat.lib.whu.edu.cn/freeBook/ajaxGetTime'
        headers5 = {
            'Host': 'seat.lib.whu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Referer': 'http://seat.lib.whu.edu.cn/'
        }

        # dfId = pd.read_csv('id.csv', index_col=0, encoding='gbk')
        ids = [str(s.split('_')[-1]) for s in self.dfId['id']]

        start = datetime(self.date.year, self.date.month, self.date.day, 7, 30)
        end = datetime(self.date.year, self.date.month, self.date.day, 21, 30)
        timeRange = pd.date_range(start=start, end=end, freq='30min')
        timeRange = [str(t.strftime('%H:%M')) for t in timeRange]

        dfInfo = pd.DataFrame(np.nan, index=ids, columns=['seatName','now'] + timeRange)
        for i, id in enumerate(ids):
            postdata5 = {'id': str(id), 'date': self.date.strftime('%Y-%m-%d')}
            r5 = self.session.post(urlSeat, data=postdata5, headers=headers5)
            content5 = r5.content
            soup5 = BeautifulSoup(content5, 'lxml')
            lis = soup5.find_all('li')
            availableTime = [li.text for li in lis]

            availableTime = [str(a) if len(a) == 5 else 'now' for a in availableTime]
            # TODO: if this seat is available for the whole day,book it and exit,and otherwise continue the following process
            dfInfo.loc[str(id),'seatName']=self.dfId[self.dfId['id']=='seat_'+id]['area'].values[0]+self.dfId[self.dfId['id']=='seat_'+id]['seatNumber'].values[0]
            dfInfo.loc[str(id), availableTime] = 1
            print 'Getting seat informations >>>%s/%s:%s' % (i + 1, len(ids), id)
        dfInfo.to_csv(os.path.join(self.path,'available','%s.csv'%datetime.now().strftime('%Y%m%d-%H%M%S')),encoding='gbk')
        return dfInfo

    def saveData(self):
        dir1=os.path.join(self.path,'current')
        dir2=os.path.join(self.path,'available')

        if not os.path.exists(dir1):
            os.makedirs(dir1)
        if not os.path.exists(dir2):
            os.makedirs(dir2)


        while True:
            try:
                self.getIds()
                self.getSeatInfo()
            except:
                self.login()
                self.getIds()
                self.getSeatInfo()

if __name__=='__main__':
    username='2016201050151'
    password='100779'
    path=r'd:\seatLib'
    #path=r'/root/libSeat/data'
    seat=BookSeat(username,password,path)











