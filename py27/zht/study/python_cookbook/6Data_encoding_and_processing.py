# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 08:39:41 2016

@author: hp
"""

#Writing CSV data
import csv
headers=['symbol','price','date','time','change','volume']
rows=[('aa',39.56,'6/11/2007','9:36am',-0.15,181800),
      ('aig',78.24,'6/11/2007','9:36am',-0.18,195500),
      ('axp',42.24,'6/11/2007','9:36am',-0.18,95500)
      ]
with open('stock.csv','w') as f:
    f_csv=csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)


'''
if you have the data as a sequence of dictionaries,do this:
'''
headers=['symbol','price','date','time','change','volume']
rows=[
    {'symbol': 'aa', 'volume': '181800', 'time': '9:36am', 'date': '6/11/2007', 'price': '39.56', 'change': '-0.15'},
    {'symbol': 'aig', 'volume': '195500', 'time': '9:36am', 'date': '6/11/2007', 'price': '78.24', 'change': '-0.18'},
    {'symbol': 'axp', 'volume': '95500', 'time': '9:36am', 'date': '6/11/2007', 'price': '42.24', 'change': '-0.18'}
    ]

with open('stock.csv','w') as f:
    f_csv=csv.DictWriter(f,headers)
    f_csv.writeheader()
    f_csv.writerows(rows)


#Reading CSV data
import csv
with open('stock.csv') as f:
    f_csv=csv.reader(f)
    headers=next(f_csv)
    for row in f_csv:
        print row


from collections import namedtuple
with open('stock.csv') as f:
    f_csv=csv.reader(f)
    headings=next(f_csv)
    Row=namedtuple('Row',headings)
    for r in f_csv:
        row=Row(*r)
        print row
'''
This would allow you to use the column headers such as row.symbol
and row.change instead of indices.
'''

import csv
with open('stock.csv') as f:
    f_csv=csv.DictReader(f)
    for row in f_csv:
        print row
'''
This method will read the data as a sequence of dictionaries instead.
'''


#example of reading tag-separated values
with open('stock.tsv') as f:
    f_tsv=csv.reader(f,delimiter='\t')
    for row in f_tsv:
        #process data
        pass

'''
If you're reading CSV data and converting it into named tuples,
you need to be a little careful with validating column headers.
For example,a CSV file could have a header line containing nonvalid
identifier characters like this:
    Street Address,Num-Premises,Latitude,Longitude
This will actually cause the creation of a namedtuple to fail with a
ValueError exception.To work around this ,you might have to scrub the
headers first.For instance,carrying a regex substitution on nonvalid
identifier characters like this:
'''
import re
with open('stock.csv') as f:
    f_csv=csv.reader(f)
    headers=[re.sub('[^a-zA-Z_]','_',h) for h in next(f_csv)]
    Row=namedtuple('Row',headers)
    for r in f_csv:
        row=Row(*r)
        #process row
        pass


#Interacting with a relational database
stocks=[
        ('goog',100,490.1),
        ('aapl',50,545.75),
        ('fb',150,7.45),
        ('hpq',75,33.2)
        ]
import sqlite3
db=sqlite3.connect("database.db")
c=db.cursor()
c.execute('create table portfolio (symbol text,shares integer,price real)')
db.commit()
c.executemany('insert into portfolio values (?,?,?)',stocks)
db.commit()
for row in db.execute('select * from portfolio'):
    print row



