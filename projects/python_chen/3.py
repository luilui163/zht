# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-09-26  18:44
# NAME:zht-3.py
import pandas as pd
import numpy as np

def weighted_grade():
    df=pd.read_csv(r'e:\a\final grades.csv')
    df=df.iloc[:,:4]
    weights=[0.1,0.1,0.1,0.7]

    df['grade']=df.values @ np.array(weights)
    df=df.sort_values('grade')


def table_9x9():
    table1=''
    for i in range(1,10):
        for j in range(1,i+1):
            cell=f'{i}x{j}={i*j}'
            table1+=f'{cell:<8}'
        table1+='\n'

    # table2='\n'.join([''.join([f'{i}x{j}={i*j:<3}' for i in range(1,j+1)]) for j in range(1,10)])
    print(table1)


def lambda_filter():
    s=[['apple','orange'],['peach','pear'],['opal','ruby'],['topaz','turquoise']]
    print(list(filter(lambda x:x[0][0]==x[1][0],s)))

def login():
    pass

def while_login():
    accounts={}
    i=0
    while i<3:
        name,psw=input('请输入账号和密码：')
        if accounts[name]==psw:
            login()
            print('登陆成功！')
            break
        else:
            i+=1
    if i==3:
        print(f'密码连续三次错误，账号已被锁定！')


