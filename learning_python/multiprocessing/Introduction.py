# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-04-17  23:08
# NAME:zht-Introduction.py


from multiprocessing import Pool,Process,Queue,Lock

'''

def f(q):
    q.put([42,None,'hello'])

if __name__=='__main__':
    q=Queue()
    p=Process(target=f,args=(q,))
    p.start()
    print(q.get())
    p.join()
'''

def f(l,i):
    l.acquire()
    try:
        print('hello, world',i)
    finally:
        l.release()

if __name__=='__main__':
    lock=Lock()

    for num in range(10):
        Process(target=f,args=(lock,num)).start()
