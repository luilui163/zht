# -*- coding: utf-8 -*-
"""
Created on Sat Aug 06 12:45:45 2016

@author: hp
"""
import urllib2
from bs4 import BeautifulSoup
import time
import threading
import Queue


class Proxy_xici:
    def __init__(self,filename,page_num=5,multithread_num=20):
        self.page_num=page_num
        self.filename=filename
        self.q_proxys=Queue.Queue()
        self.checked_proxys=[]
        self.lock=threading.Lock()
        self.multithread_num=multithread_num
        
    def get_proxy(self):
        for page in range(1,self.page_num+1):
            headers={
                    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
                    }
            url=r'http://www.xicidaili.com/nt/'+str(page)
            req=urllib2.Request(url,headers=headers)
            content=urllib2.urlopen(req).read()
            soup=BeautifulSoup(content)
            items=soup.find_all('tr',{'class':'odd'})
            for item in items:
                tds=item.find_all('td')
                addr=tds[1].string
                port=tds[2].string    
                self.q_proxys.put(addr+':'+port)
            print 'page',page

    def check_proxy(self):
        while not self.q_proxys.empty():
            self.lock.acquire()
            p=self.q_proxys.get()
            self.lock.release()
            try:
                proxy={'http':p}
                proxy_support=urllib2.ProxyHandler(proxy)
                opener=urllib2.build_opener(proxy_support)
                urllib2.install_opener(opener)
                headers={
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
                        }
                url='https://www.baidu.com/'
                mark='11000002000001'
                t1=time.time()
                req=urllib2.Request(url,headers=headers)
                content=urllib2.urlopen(req,timeout=5).read()
                timeused=time.time()-t1
                if content.find(mark)>-1:
                    print p,timeused
                    self.lock.acquire()
                    self.checked_proxys.append((p,timeused))
                    self.lock.release()
                    
                else:
                    p,'is invalid!!!!!!!!!!!!!'
            except urllib2.URLError as e:
                print p,e.reason

            
    def multithread_check(self):
        ts=[]
        for _ in range(self.multithread_num):
            t=threading.Thread(target=self.check_proxy)
            t.start()
            ts.append(t)
        for th in ts:
            th.join()

    def sort(self):
        self.checked_proxys.sort(key=lambda x:x[1])#form small to big one
    
    def save(self):
        with open(self.filename,'w') as f:
            for p in self.checked_proxys:
                f.write('%s\t%f\n'%(p[0],p[1]))
    
    def run(self):
        self.get_proxy()
        self.multithread_check()
        self.sort()
        self.save()
        
if __name__=='__main__':
    p=Proxy_xici(page_num=20,filename=r'E:\51job\file\%d.txt'%int(time.time()))
    p.run()
