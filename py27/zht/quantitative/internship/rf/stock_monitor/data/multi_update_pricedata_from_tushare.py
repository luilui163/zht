#-*-coding: utf-8 -*-
#@author:tyhj
import pandas as pd
import datetime
import os
import tushare as ts
import threading
from Queue import Queue

#==================================================================
import logging
import logging.handlers

log_name=str(datetime.datetime.today().strftime('%Y%m%d'))
LOG_FILE=r'C:\zht\OneDrive\script\rf\stock_monitor\log\%s.log'%log_name
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
formatter = logging.Formatter(fmt)   # 实例化formatter
handler.setFormatter(formatter)      # 为handler添加formatter
logger = logging.getLogger(log_name)    # 获取名为tst的logger
logger.addHandler(handler)           # 为logger添加handler
logger.setLevel(logging.DEBUG)

codes_wrong=[]

def get_codes():
    df = ts.get_stock_basics()
    codes= df.index.tolist()
    return codes

def update_data(code,code_id):
    new_date=datetime.datetime.today()
    new_date=new_date.strftime('%Y-%m-%d')
    file_name = r'C:\zht\OneDrive\script\rf\stock_monitor\sina\%s.csv' % code
    if os.path.exists(file_name):
        df = pd.read_csv(file_name, index_col=0)
        old_date = df.index[-1]
        df.index = [pd.Timestamp(ind) for ind in df.index]
        data = ts.get_h_data(code, start=old_date, end=new_date,autype='qfq',retry_count=100,)
        data = data.sort_index(ascending=True)
        df.drop(df.index[-1], inplace=True)
        df = df.append(data)
        df.to_csv(file_name)
    else:
        df=ts.get_h_data(code,start='2005-01-01',end=new_date,retry_count=100,autype='qfq')
        if not df.empty:
            df = df.sort_index(ascending=True)
            df.to_csv(file_name)
    logger.info('%s-%s-%s'%(code,code_id,threading.active_count()-1))
    print code,code_id,threading.activeCount()-1

def _job(q):
    while not q.empty():
        code=q.get()
        code_id=q.qsize()
        try:
            update_data(code,code_id)
        except Exception,e:
            logger.error('%s-%s-%s-error,%s'%(code,code_id,threading.active_count()-1,e))
            if e=='timed,out':
                codes_wrong.append(code)
                q.put(code)

def mul_update_data(mul_number):
    codes=get_codes()
    q=Queue()
    for code in codes:
        q.put(code)

    ths=[]
    for i in range(mul_number):
        th=threading.Thread(target=_job,args=[q])
        ths.append(th)
    for th in ths:
        th.start()
    for th in ths:
        th.join()

# def get_codes():
#     files=os.listdir(r'C:\zht\OneDrive\script\rf\stock_monitor\sina')
#     codes=[f[:-4] for f in files]
#     codes.sort()
#     return codes

mul_update_data(50)
print '\n\nfinished!'
with open(r'C:\zht\OneDrive\script\rf\stock_monitor\log\wrong_codes.txt','w') as f:
    for cw in codes_wrong:
        f.write(cw+'\n')


#TODO:the logic of initialize new df or update data

# def update_data():
#     new_date=datetime.datetime.today()
#     new_date=new_date.strftime('%Y-%m-%d')
#     codes=get_codes()
#     for code in codes:
#         file_name = r'C:\zht\OneDrive\script\rf\stock_monitor\sina\%s.csv' % code
#         df=pd.read_csv(file_name,index_col=0)
#         old_date = df.index[-1]
#         df.index=[pd.Timestamp(ind) for ind in df.index]
#         data=ts.get_h_data(code, start=old_date,end=new_date)
#         data=data.sort_index(ascending=True)
#         df.drop(df.index[-1],inplace=True)
#         df=df.append(data)
#         df.to_csv(file_name)
#         print code



'''
def get_former_date():
    codes=get_codes()
    for i in range(10):
        file_name = r'C:\zht\OneDrive\script\rf\stock_monitor\sina\%s.csv' % code
        df = pd.read_csv(file_name, index_col=0)


# df.index=[pd.Timestamp(ind) for ind in df.index]



def formatting_df(code):
    file_name=r'C:\zht\OneDrive\script\rf\stock_monitor\sina\%s.csv'%code
    df=pd.read_csv(file_name,index_col=0)
    df=df.sort_index(ascending=True)
    new_ind=[''.join(ind.split('-')) for ind in df.index]
    new_ind=[datetime.datetime.strptime(ind,'%Y%m%d') for ind in new_ind]
    new_ind=[pd.Timestamp(ind) for ind in new_ind] #change the format of indext to pd.Timestamp
    df.index=new_ind
    df.to_csv(file_name)


def formatting_all_dfs():
    codes=get_codes()
    for code in codes:
        formatting_df(code)
        print code

formatting_all_dfs()

def get_former_date():
    codes=get_codes()
    former_date=0
    for code in codes[:10]:
        file_name = r'C:\zht\OneDrive\script\rf\stock_monitor\sina\%s.csv' % code
        df=pd.read_csv(file_name,index_col=0)
        df.index = [pd.Timestamp(nd) for nd in df.index]



df1=datahandler.get_data('000009.SZ')




df2=pd.read_csv(r'C:\zht\OneDrive\script\rf\stock_monitor\marketdata\000009.SZ.csv',index_col=0)

'''