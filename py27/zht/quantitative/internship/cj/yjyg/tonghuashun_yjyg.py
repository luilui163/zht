#-*-coding: utf-8 -*-
#@author:tyhj
'''
API:
url=r'http://data.10jqka.com.cn/financial/yjyg/date/%s/board/ALL/field/enddate/order/desc/page/%d/ajax/1/'%(date,page)
'''

import MySQLdb
import os
import chardet
import urllib2
from bs4 import BeautifulSoup
import time
import random
import chardet
import Queue
import sys

db=MySQLdb.connect(host='localhost',user='root',,db='yjyg',charset='utf8')
cursor=db.cursor()
cursor.execute('SET NAMES utf8')
sql_create_table='''
                CREATE TABLE IF NOT EXISTS tonghuashun(
                quarter TEXT,
                code CHAR(6),
                name TEXT,
                performance TEXT,
                net_profit_fluctuation TEXT,
                type TEXT,
                profit_of_last_year TEXT,
                announcement_date DATE,
                PRIMARY KEY(code,announcement_date)
                )ENGINE=INNODB CHARSET=UTF8;
                '''
cursor.execute(sql_create_table)


# url=r'http://data.10jqka.com.cn/financial/yjyg/date/2016-12-31/ajax/2/'
def get_total_pages(quarter):
    date=get_complete_date(quarter)
    url=r'http://data.10jqka.com.cn/financial/yjyg/date/%s/board/ALL/field/enddate/order/desc/page/1/ajax/1/'%date
    content=urllib2.urlopen(url).read()
    soup=BeautifulSoup(content,'lxml')
    try:
        total_pages=soup.findAll('span',{'class':'page_info'})[0].string.split('/')[-1]
    except:
        total_pages=1
    return total_pages

def get_complete_date(quarter):
    year,month=quarter[:4],quarter[4:]
    mp={'03':'31','06':'30','09':'30','12':'31'}
    return year+'-'+month+'-'+mp[month]

def parse_data(quarter,page):
    date=get_complete_date(quarter)
    url=r'http://data.10jqka.com.cn/financial/yjyg/date/%s/board/ALL/field/enddate/order/desc/page/%d/ajax/1/'%(date,page)
    content=urllib2.urlopen(url).read()
    soup=BeautifulSoup(content,'lxml')
    tbody=soup.findAll('tbody')[0]
    trs=tbody.findAll('tr')
    data=[]
    for tr in trs:
        a_s=tr.findAll('a')
        code,name,performance=[a.string for a in a_s]
        tds=tr.findAll('td')
        net_profit_fluctuation,profit_of_last_year,announcement_date=[td.string for td in tds[-3:]]
        span=tr.findAll('span')[0]
        type=span.string
        ticker=(quarter,code,name,performance,net_profit_fluctuation,type,profit_of_last_year,announcement_date)
        data.append(ticker)
    return data

def get_quarters():
    url=r'http://data.10jqka.com.cn/financial/yjyg/'
    content=urllib2.urlopen(url).read()
    soup=BeautifulSoup(content,'lxml')
    ul=soup.findAll('ul',{'class':'list'})[0]
    a_s=ul.findAll('a')
    quarters=[a.string for a in a_s]
    mp={u'年年报':'12',u'年一季报':'03',u'年三季报':'09',u'年中报':'06'}
    quarters=[q[:4]+mp[q[4:]] for q in quarters]
    return quarters

def write_into_mysql(data):
    for ticker in data:
        sql_insert='''insert tonghuashun(quarter,code,name,type,performance,net_profit_fluctuation,profit_of_last_year,announcement_date)
        values('%s','%s','%s','%s','%s','%s','%s','%s')'''%ticker
        try:
            cursor.execute(sql_insert)
            db.commit()
        except:
            info = sys.exc_info()[1].args
            if info[0] == 1062:
                print info[1]
                pass


def run():
    q = Queue.LifoQueue()
    quarters=get_quarters()
    for quarter in quarters:
        total_pages=get_total_pages(quarter)
        for i in range(1,int(total_pages)+1):
            q.put((quarter,i))

    while not q.empty():
        task=q.get()
        try:
            data=parse_data(task[0],task[1])
            write_into_mysql(data)
            print task[0],task[1]
        except:
            time.sleep(random.random())
            q.put(task)

    cursor.close()
    db.close()

if __name__=='__main__':
    run()





