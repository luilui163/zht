# -*-coding: utf-8 -*-
# @author:tyhj

# using firefox to analyse the html
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
from datetime import datetime, timedelta


class Seat:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()
        self.login()
        self.date = datetime.today()
        self.dfId = self.getIds()
        self.now = datetime.now()
        self.dfInfo = self.getSeatInfo()
        self.grade = self.rankSeats()
        self.mapId, self.mapTime = self.getMap()
        self.bookSeat()

    def getCookies(self):
        # get the cookies
        urlMain = r'http://seat.lib.whu.edu.cn/login?targetUri=/'
        headers1 = {
            'Host': 'seat.lib.whu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
        }

        self.session.get(urlMain)
        r1 = self.session.get(urlMain)

    def getCaptcha(self):
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

    def _detectCaptcha(self, content):
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
        self.getCookies()
        urlSignin = r'http://seat.lib.whu.edu.cn/auth/signIn'
        headers3 = {
            'Host': 'seat.lib.whu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
        }
        postdata3 = {
            'username': self.username,
            'password': self.password,
            'captcha': self.getCaptcha()
        }

        r3 = self.session.post(urlSignin, data=postdata3, headers=headers3)

        if len(r3.content) > 10000:
            # print 'the captcha is:%s' % self.captcha
            print 'login in successfully!'
        else:
            print 'the captcha is wrong,it is logining in again!'
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
            urlSeatList = r'http://seat.lib.whu.edu.cn/freeBook/ajaxSearch?onDate=%s&building=1&room=&hour=null&power=null&startMin=null&endMin=null&offset=%s' % (
                self.date.strftime('%Y-%m-%d'), offset)
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
        return dfId

    def getSeatInfo(self):
        # get the informations of all the seats
        now = self.now
        point1 = datetime(now.year, now.month, now.day, 21, 30)
        point2 = datetime(now.year, now.month, now.day, 22, 30)
        if now >= point2:
            # book for the next day
            self.date += timedelta(days=1)
        elif now >= point1:
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

        dfInfo = pd.DataFrame(np.nan, index=ids, columns=['now'] + timeRange)

        for i, id in enumerate(ids):
            postdata5 = {'id': str(id), 'date': self.date.strftime('%Y-%m-%d')}
            r5 = self.session.post(urlSeat, data=postdata5, headers=headers5)
            content5 = r5.content
            soup5 = BeautifulSoup(content5, 'lxml')
            lis = soup5.find_all('li')
            availableTime = [li.text for li in lis]

            availableTime = [str(a) if len(a) == 5 else 'now' for a in availableTime]
            # TODO: if this seat is available for the whole day,book it and exit,and otherwise continue the following process

            dfInfo.loc[str(id), availableTime] = 1
            print 'Getting seat informations >>>%s/%s:%s' % (i + 1, len(ids), id)
        return dfInfo

    def rankSeats(self):
        # rank the available seats
        '''
        factors:
        continuity
        time interval
        right now?
        break point?
        '''
        grade = self.dfInfo
        grade = grade.dropna(axis=1, how='all')
        tmp = grade.fillna(0)
        s = tmp.cumprod(axis=1)
        grade['grade'] = s.sum(axis=1)
        # grade=grade.sort_values('grade',ascending=False)
        # # grade=grade.dopna(axis=1,how='all')
        # grade.to_csv('grade.csv')

        prioritySeats = open('prioritySeats.txt').read().split('\n')

        grade['priority'] = False
        # if len(set(grade.index.tolist()).intersection(set(prioritySeats)))>0:
        #     grade.loc[prioritySeats, 'priority'] = True
        grade = grade.sort_values(['priority', 'grade'], ascending=False)
        # grade.to_csv('grade.csv')
        return grade

    def getMap(self):
        mapId = {self.dfId['id'][i][-4:]: (self.dfId['seatNumber'][i], self.dfId['area'][i]) for i in
                 range(self.dfId.shape[0])}
        if self.grade.columns[0] == 'now':
            mapTime = {t: str(int(t.split(':')[0]) * 60 + int(t.split(':')[1])) for t in self.grade.columns[1:-2]}
        else:
            mapTime = {t: str(int(t.split(':')[0]) * 60 + int(t.split(':')[1])) for t in self.grade.columns[:-2]}

        return mapId, mapTime

    def bookSeat(self):
        # book seat
        urlBook = r'http://seat.lib.whu.edu.cn/selfRes'
        headers6 = {
            'Host': 'seat.lib.whu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Referer': 'http://seat.lib.whu.edu.cn/'
        }

        # TODO:random choice
        i = 0
        while True:
            target = self.grade.ix[i]
            id = target.name
            if target.index[0] == 'now':
                start = 'now'
            else:
                start = self.mapTime[target.index[0]]
            end = self.mapTime[target.index[target[-2] - 1]]

            postdata6 = {
                'date': self.date.strftime('%Y-%m-%d'),
                'seat': id,
                'start': start,
                'end': end,
                'captcha': ''
            }

            r6 = self.session.post(urlBook, data=postdata6, headers=headers6)
            # print r6.content
            if '凭证号' in r6.content:
                print 'seat [%s] in [%s] has been booked for you' % tuple(self.mapId[id])
                break
            elif '已有1个有效预约' in r6.content:
                print 'you have booked a seat,can not book again!!'
                print '\nAre you want to stop using the current seat and book another seat?'
                self.stopUsing()
                break
            else:
                i += 1

    def stopUsing(self):
        url = r'http://seat.lib.whu.edu.cn/user/stopUsing'
        headers = {
            'Host': 'seat.lib.whu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Referer': 'http://seat.lib.whu.edu.cn/history?type=SEAT'
        }
        r = self.session.get(url, headers=headers)
        if '成功停止使用当前预约' in r.content:
            print 'you have stopped using seat'


if __name__ == '__main__':
    username = '2016201050151'
    password = '100779'
    seat = Seat(username, password)
    seat.dfInfo.to_csv(r'D:\seatLib\info\info_%s.csv' % datetime.now().strftime('%Y%m%d-%H%M%S'))


# TODO:multithreading

# TODO:1,automatically manage the seats using available accounts;
# TODO:2,monitor the library,such as the summit,time to go lunch,and so on.
# TODO:3,analyse the history to rank the most popular seats
# TODO:4,automatically book seats for partners
# TODO:5,send mail using yagmail
# TODO:6,setting the start time and end time
# TODO:7,why 16:30,rather than 17:00?


# TODO: do not need to login again unless the cookies has expired,and do not need to parse the path of every seat
