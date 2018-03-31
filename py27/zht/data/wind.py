#-*-coding: utf-8 -*-
#@author:tyhj
import os
import pandas as pd
import datetime
from util import dateu


from WindPy import *
w.start()

def get_SW_first_industry():
    data1=w.wset("sectorconstituent","date=2017-03-06;sectorid=a39901011g000000")
    wind_codes=data1.Data[1]
    wind_names=data1.Data[2]
    z=zip(wind_codes,wind_names)

    dates=pd.date_range('2005-01-01','2017-03-05',freq='M')
    dates=[d.strftime('%Y-%m-%d') for d in dates]

    for date in dates:
        if not os.path.isdir(os.path.join(r'C:\data\SW_sector',date)):
            os.makedirs(os.path.join(r'C:\data\SW_sector',date))
        for wind_code,wind_name in z:
            data = w.wset("sectorconstituent", "date=%s;windcode=%s" % (date, wind_code))
            df=pd.DataFrame(data.Data,index=['time','code','name'])
            df=df.T
            df=df.set_index('code')
            del df['time']
            df.to_csv(os.path.join(r'c:\data\SW_sector',date,wind_name+'.csv'),encoding='gbk')
        print date

def get_index(indName='000300.SH'):
    today = datetime.today().strftime('%Y-%m-%d')
    wdata=w.wsd("%s"%indName, "open,high,low,close,volume,amt", "2001-01-01", "%s"%today)
    dates = [t.strftime('%Y-%m-%d') for t in wdata.Times]
    tickers="open,high,low,close,volume,amt".split(',')
    df = pd.DataFrame(wdata.Data, index=tickers, columns=dates)
    df=df.T
    df=df.dropna(axis=0,how='any')
    df.to_csv(r'C:\db\mkt\daily\index\%s.csv'%(indName.split('.')[0]))

def getAllStockIds():
    '''
    get all the listed stock ids until today
    :return:
    '''
    today = dateu.getToday()
    path=r'D:\quantDb\mkt\dataset\stockIds\%s.txt'%today
    if not os.path.exists(path):
        data=w.wset("sectorconstituent","date=%s;sectorid=a001010100000000"%today)
        allStockIds=data.Data[1]
        with open(path, 'w') as f:
            f.write('\n'.join(allStockIds))
        return allStockIds
    else:
        allStockIds=open(path).read().split('\n')
        return allStockIds

def getMktCap(sdate=None,edate=None):
    '''
    get total market value,price is adjusted forwardly

    :param sdate:
    :param edate:
    :return:pandas dataframe
    '''
    if not sdate:
        sdate=dateu.int2Date(1990,01,01)
    if not edate:
        edate=dateu.getToday()

    allStockIds=getAllStockIds()
    data=w.wsd("%s"%(','.join(allStockIds)), "mkt_cap_ard",
                sdate, edate, "unit=1;Period=Y;PriceAdj=F")

    df=pd.DataFrame(data.Data,index=data.Codes,columns=data.Times)
    df=df.T
    df.index=[ind.to_pydatetime().strftime('%Y-%m-%d') for ind in df.index]
    # df.to_csv(r'D:\quantData\mkt_cap_qfq.csv')
    return df

#定向增发预案公告日
def get_dz():
    codes=data_handler.get_code_list()
    year_end=datetime.today().year
    df=pd.DataFrame(index=codes)
    for year in range(2005,year_end+1):
        winddata=w.wss(','.join(codes), "fellow_preplandate","year=%d"%year)
        data=winddata.Data[0]
        dates=[]
        for d in data:
            if d.year<1900:
                dates.append(np.NaN)
            else:
                dates.append(d.strftime('%Y-%m-%d'))
        df[year]=dates
        print year

    dir=os.path.join(tool.dirpath,'data')
    if not os.path.exists(dir):
        os.makedirs(dir)

    df.to_csv(os.path.join(dir,'dz.csv'))

#限售股解禁日期
def get_jj():
    codes = data_handler.get_code_list()
    today=datetime.today().strftime('%Y-%m-%d')
    month_ends=pd.date_range(start='2005-01-01',end=today,freq='M')
    month_ends=[d.strftime('%Y%m%d') for d in month_ends]
    df=pd.DataFrame(index=codes)
    for month_end in month_ends:
        #该函数拿到的数据是在tradeDate之前最近一次解禁日期
        winddata=w.wss(','.join(codes),  "share_rtd_unlockingdate","tradeDate=%s"%month_end)
        data = winddata.Data[0]
        dates = []
        for d in data:
            if d.year < 1900:
                dates.append(np.NaN)
            else:
                dates.append(d.strftime('%Y-%m-%d'))
        df[month_end] = dates
        print month_end

    dir = os.path.join(tool.dirpath, 'data')
    if not os.path.exists(dir):
        os.makedirs(dir)

    df.to_csv(os.path.join(dir,'jj.csv'))

#业绩预告日期
def get_yjyg():
    codes = data_handler.get_code_list()
    today = datetime.today().strftime('%Y-%m-%d')
    quarters = pd.date_range(start='2005-01-01', end=today, freq='Q')
    quarters=[q.strftime('%Y%m%d') for q in quarters]
    df = pd.DataFrame(index=codes)
    for quarter in quarters:
        winddata = w.wss(','.join(codes), "profitnotice_date", "rptDate=%s" % quarter)
        data = winddata.Data[0]
        dates = []
        for d in data:
            if d.year < 1900:
                dates.append(np.NaN)
            else:
                dates.append(d.strftime('%Y-%m-%d'))
        df[quarter] = dates
        print quarter

    dir = os.path.join(tool.dirpath, 'data')
    if not os.path.exists(dir):
        os.makedirs(dir)

    df.to_csv(os.path.join(dir, 'yjyg.csv'))

#业绩预告类型
def get_yjyglx():
    codes = data_handler.get_code_list()
    today = datetime.today().strftime('%Y-%m-%d')
    quarters = pd.date_range(start='2005-01-01', end=today, freq='Q')
    quarters=[q.strftime('%Y%m%d') for q in quarters]
    df = pd.DataFrame(index=codes)
    for quarter in quarters:
        winddata = w.wss(','.join(codes), "profitnotice_style", "rptDate=%s" % quarter)
        data = winddata.Data[0]
        df[quarter] = data
        print quarter

    dir = os.path.join(tool.dirpath, 'data')
    if not os.path.exists(dir):
        os.makedirs(dir)

    df.to_csv(os.path.join(dir, 'yjyglx.csv'),encoding='gbk')

#分红送股 (高送转)
#wind获取方式：股票-专题统计-沪深股市-公司研究-分红实施


#业绩快报日期
def get_yjkb_date():
    codes = data_handler.get_code_list()
    today = datetime.today().strftime('%Y-%m-%d')
    quarters = pd.date_range(start='2005-01-01', end=today, freq='Q')
    quarters = [q.strftime('%Y%m%d') for q in quarters]
    df = pd.DataFrame(index=codes)
    for quarter in quarters:
        winddata = w.wss(','.join(codes), "performanceexpress_date", "rptDate=%s" % quarter)
        data = winddata.Data[0]
        dates = []
        for d in data:
            if d.year < 1900:
                dates.append(np.NaN)
            else:
                dates.append(d.strftime('%Y-%m-%d'))
        df[quarter] = dates
        print quarter

    dir = os.path.join(tool.dirpath, 'data')
    if not os.path.exists(dir):
        os.makedirs(dir)

    df.to_csv(os.path.join(dir, 'yjkb_date.csv'))

#业绩快报营业利润
def get_yjkb_yylr():
    codes = data_handler.get_code_list()
    today = datetime.today().strftime('%Y-%m-%d')
    quarters = pd.date_range(start='2005-01-01', end=today, freq='Q')
    quarters = [q.strftime('%Y%m%d') for q in quarters]
    df = pd.DataFrame(index=codes)
    for quarter in quarters:
        winddata = w.wss(','.join(codes), "performanceexpress_perfexprofit", "rptDate=%s;unit=1" % quarter)
        data = winddata.Data[0]
        df[quarter] = data
        print quarter

    dir = os.path.join(tool.dirpath, 'data')
    if not os.path.exists(dir):
        os.makedirs(dir)

    df.to_csv(os.path.join(dir, 'yjkb_yylr.csv'))


#流通市值(不复权)
def get_mkt_cap_float():
    '''流通市值'''
    stockIds=getAllStockIds()
    today = dateu.getToday()
    data=w.wsd(','.join(stockIds), "mkt_cap_float", "1999-01-01", today,
          "unit=1;currencyType=;Period=M")
    df=pd.DataFrame(data.Data,index=data.Codes,columns=data.Times)
    df=df.T
    df.index=[ind.to_pydatetime().strftime('%Y-%m-%d') for ind in df.index]
    # df.to_csv('D:\quantDb\mkt\monthly\mkt_cap_float.csv')
    return df

#每股净资产
def get_wgsd_bps(stockIds,start,end):
    '''每股净资产'''
    # stockIds=open(r'D:\quantDb\mkt\dataset\stockIds\2017-07-09.txt').read().split('\n')
    # today=dateu.getToday()

    data=w.wsd(','.join(stockIds), "wgsd_bps", start, end, "currencyType=;Period=M")

    df = pd.DataFrame(data.Data, index=data.Codes, columns=data.Times)
    df = df.T
    df.index = [ind.to_pydatetime().strftime('%Y-%m-%d') for ind in df.index]
    return df



def getTS(stockIds,name,startDate="1990-01-01",endDate=datetime.today().strftime('%Y-%m-%d')):
    data=w.wsd(','.join(stockIds), name, startDate, endDate, "unit=1;rptType=1;Period=Y;Days=Alldays")

    df = pd.DataFrame(data.Data, index=data.Codes, columns=data.Times)
    df = df.T
    df.index = [ind.to_pydatetime().strftime('%Y-%m-%d') for ind in df.index]

    df.to_csv(r'D:\quantDb\researchTopics\fama\src\%s.csv'%name)
    print 'saved %s'%name

stockIds=getAllStockIds()
# getTS(stockIds,'selling_dist_exp')
# getTS(stockIds,'fin_exp_is')
# getTS(stockIds,'gerl_admin_exp')
# getTS(stockIds,'tot_equity')
# getTS(stockIds,'wgsd_assets')

#总资产
def wgsd_assets():
    name='wgsd_assets'
    startDate='1990-01-01'
    endDate=datetime.today().strftime('%Y-%m-%d')

    data=w.wsd(','.join(stockIds), "wgsd_assets", "1990-01-01", "2017-07-22", "unit=1;rptType=1;currencyType=;Period=Y;Days=Alldays")
    df = pd.DataFrame(data.Data, index=data.Codes, columns=data.Times)
    df = df.T
    df.index = [ind.to_pydatetime().strftime('%Y-%m-%d') for ind in df.index]

    df.to_csv(r'D:\quantDb\researchTopics\fama\src\%s.csv' % name)

