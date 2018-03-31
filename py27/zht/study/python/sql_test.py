# -*- coding: utf-8 -*-
"""
Created on Thu May 26 10:03:44 2016

@author: Administrator
"""
#http://www.cnblogs.com/fnng/p/3565912.html


import MySQLdb
conn=MySQLdb.connect(
                    host='192.168.1.242',
                    port=3306,
                    user='quant_user',
                    passwd='sftz',
                    db='juling')
cur=conn.cursor()

cur.execute('select * from ana_indu_expr_idx')
stus=cur.fetchall()





#cur.close()
#conn.close()