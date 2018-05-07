#-*-coding: utf-8 -*-
#@author:tyhj

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


db=MySQLdb.connect(host='localhost',user='root',passwd=,db='yjyg',charset='utf8')
cursor=db.cursor()
cursor.execute('SET NAMES utf8')

#create a table named dongcai in database yjyg
sql_create_table='''
                CREATE TABLE IF NOT EXISTS dongcai(
                quarter TEXT,
                code CHAR(6),
                name TEXT,
                performance TEXT,
                performance_data TEXT,
                type TEXT,
                profit_of_last_year TEXT,
                announcement_date DATE,
                PRIMARY KEY(code,announcement_date)
                )ENGINE=INNODB CHARSET=UTF8;
                '''
cursor.execute('drop table if exists dongcai')
cursor.execute(sql_create_table)

def get_soup(url):
    content=urllib2.urlopen(url).read()
    soup=BeautifulSoup(content,'lxml')
    return soup

def get_total_pages(soup):
#get number of total pages
    div=soup.findAll('div',{'class':'Page','id':'PageCont'})
    if div!=[]:
        total_pages=div[0].findAll('a',{'title':'转到最后一页'})[0].string
    else:
        total_pages=1
    return total_pages

def parse_data(soup):
    tbody = soup.findAll('tbody')
    trs = tbody[0].findAll('tr')
    data=[]
    for tr in trs[::-1]:
        tick = []
        tds = tr.findAll('td')
        for i, td in enumerate(tds):
            if i == 4:
                performance = ''
                for s in td.strings:
                    performance += s.strip()
                tick.append(performance)
            else:
                if td.string!=None:
                    tick.append(td.string)
                else:
                    tick.append('-')
        data.append(tick)
    return data

def crawler(quarter):
    url = r'http://data.eastmoney.com/soft_new/bbsj/%s/yjyg.html'%quarter
    soup = get_soup(url)
    total_pages = get_total_pages(soup)
    #get the data by descending sequence
    if total_pages >1:
        time.sleep(random.random())
        for page in range(2, int(total_pages) + 1)[::-1]:
            url = r'http://data.eastmoney.com/soft_new/bbsj/%s/yjyg/fsrq/asc/%d.html' % (quarter,page)
            soup = get_soup(url)
            data = parse_data(soup)
            write_into_mysql(quarter,data)
            print quarter,page

    #get the data of the first page
    url = r'http://data.eastmoney.com/soft_new/bbsj/%s/yjyg.html'%quarter
    soup = get_soup(url)
    data = parse_data(soup)
    write_into_mysql(quarter,data)
    print quarter,1

def write_into_mysql(quarter,data):
    for d in data:
        tmp_d=[m.encode('gbk') for m in d]
        sql_insert='''
        insert dongcai(quarter,code,name,performance,performance_data,type,profit_of_last_year,
        announcement_date) values('%s','%s','%s','%s','%s','%s','%s','%s')
        '''%tuple([quarter]+d[1:])

        try:
            cursor.execute(sql_insert)
            db.commit()
        except:
            info = sys.exc_info()[1].args
            if info[0] == 1062:
                print info[1]
                pass

def get_quarters():
    url=r'http://data.eastmoney.com/soft_new/bbsj/201412/yjyg.html'
    content=urllib2.urlopen(url).read()
    soup=BeautifulSoup(content,'lxml')
    select=soup.findAll('select',{'class':'slt'})[0]
    options=select.findAll('option')
    date=[option.string for option in options]
    quarters=[''.join(d.split('-')[:2]) for d in date]
    #There are some invalid dates.
    quarters=[q for q in quarters if int(q[-2:])%3==0]
    return quarters

if __name__=='__main__':
    quarters = get_quarters()
    q = Queue.LifoQueue()
    for quarter in quarters:
        q.put(quarter)
    while not q.empty():
        quarter = q.get()
        try:
            crawler(quarter)
        except Exception as e:
            q.put(quarter)
            print quarter, e

    cursor.close()
    db.close()



















