# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 14:00:13 2016

@author: Administrator
"""


ap_stocks=open(r'c:\cluster\similarity\ap_20111201.txt').read().split('\n')[:-1]

lines=open(r'c:\cluster\similarity\bloomberg_20150831.txt').read().split('\n')[:-1]
bbg_stocks=[l.split('\t')[0] for l in lines]
#gx_stocks=open(r'c:\cluster\similarity\gx_20120101.txt').read().split('\n')[:-1]
#sw_stocks=open(r'c:\cluster\similarity\sw_20120101.txt').read().split('\n')[:-1]
#wind_stocks=open(r'c:\cluster\similarity\wind_20120101.txt').read().split('\n')[:-1]
#zx_stocks=open(r'c:\cluster\similarity\zx_20120101.txt').read().split('\n')[:-1]

    
#intersection_stocks=
    
def get_stocks(path):
    lines=open(path).read().split('\n')[:-1]
    stocks=[l.split('\t')[0] for l in lines]
    return stocks
gx_stocks=get_stocks(r'c:\cluster\similarity\gx_20120101.txt')
zx_stocks=get_stocks(r'c:\cluster\similarity\zx_20120101.txt')
wind_stocks=get_stocks(r'c:\cluster\similarity\wind_20120101.txt')
    
intersection_stocks=list(set(ap_stocks).intersection(set(bbg_stocks)).intersection(set(bbg_stocks)).intersection(set(ap_stocks)).intersection(set(gx_stocks)).intersection(set(zx_stocks).intersection(set(wind_stocks))))


'''
import os

def func(stock_name):
    if stock_name[-1]=='S':
        return stock_name[:-1]+'H'
    else:
        return stock_name
        
#path=r'c:\cluster\similarity\ap20111201'
#files=os.listdir(path)
#files_paths=[os.path.join(path,f) for f in files]
#for i in range(len(files_paths)):
#    f=open(r'c:\cluster\similarity\ap\%s'%files[i],'w')
#    stocks=open(files_paths[i]).read().split('\n')[:-1]
#    stocks=map(func,stocks)
#    for j in range(len(stocks)):
#        if stocks[j] in intersection_stocks:
#            f.write('%s\n'%stocks[j])
#    f.close()

lines=open(r'c:\cluster\similarity\bloomberg_20150831.txt').read().split('\n')[:-1]
stocks=[l.split('\t')[0] for l in lines]
stocks=map(func,stocks)
subindustrys=[l.split('\t')[3] for l in lines]
classification=list(set(subindustrys))
bbg_instruction=open(r'c:\cluster\similarity\bbg_instruction.txt','w')
for k in range(len(classification)):
    bbg_instruction.write('bbg%s\t%s\n'%(str(k),classification[k]))
    ff=open(r'c:\cluster\similarity\bbg\bbg%s.txt'%str(k),'w')
    for s in range(len(stocks)):
        if subindustrys[s]==classification[k] and stocks[s] in intersection_stocks:
            ff.write('%s\n'%stocks[s])
    ff.close()
bbg_instruction.close()

lines=open(r'c:\cluster\similarity\bbg_20120101.txt').read().split('\n')[:-1]
stocks=[l.split('\t')[0] for l in lines]
industrys=[l.split('\t')[3] for l in lines]
classifications=list(set(industrys))

'''








