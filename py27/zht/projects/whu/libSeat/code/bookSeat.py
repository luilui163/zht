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
    def __init__(self,username,password):
        self.username=username
        self.password=password
        self.date = datetime.today()+timedelta(days=1)
        self.run()

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

    def book(self):
        targetSeats=open(r'E:\aa\targetSeats.txt').read().split('\n')
        booked=False
        i=0
        while not booked:
            urlBook = r'http://seat.lib.whu.edu.cn/selfRes'
            headers6 = {
                'Host': 'seat.lib.whu.edu.cn',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
                'Referer': 'http://seat.lib.whu.edu.cn/'
            }

            postdata6 = {
                'date': self.date.strftime('%Y-%m-%d'),
                'seat': targetSeats[i],
                'start': '540',
                'end': '1260',
                'captcha': ''
            }

            r6 = self.session.post(urlBook, data=postdata6, headers=headers6)
            if '凭证号' in r6.content:
                booked=True
                break
            i+=1

    def run(self):
        self.login()
        self.book()

if __name__=='__main__':
    username1='2016201050151'
    password1='100779'

    username2='2016201050119'
    password2='147540'
    #path=r'/root/libSeat/data'
    seat1=BookSeat(username1,password1)
    seat2=BookSeat(username2,password2)











