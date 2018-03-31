# -*- coding: utf-8 -*-
"""
Created on Thu Sep 08 21:49:37 2016

@author: hp
"""

p=(4,5)
x,y=p
print x,y

data=['acme',50,91.9,(2012,12,21)]
name,shares,price,date=data

_,shares,price,_=data

'''star expression'''
#def drop_first_last(grades):
#    first,*middle,last=grades
#    return avg(*middle)
#
#record=('dave','dave@example.com','773-555-1212','847-555-1212')
#name,email,*phone_numbers=record
#
#print drop_first_last(record)


from collections import deque

q=deque(maxlen=3)
q.append(1)
q.append(2)
q.append(3)
print q
q.append(4)
print q

#if you dont give it a maxiumum size,you get an unbounded queue

q=deque()
q.append(1)
q.append(2)
q.appendleft(4)
print q
q.popleft()
q.pop()
print q


import heapq

nums=[1,6,3,6,23,9,48,-10,-5]
print heapq.nlargest(3,nums)
print heapq.nsmallest(2,nums)

portfolio=[
    {'name':'IBM','shares':100,'price':91.1},
    {'name':'APPL','shares':50,'price':543.2},
    {'name':'YHOO','shares':200,'price':31.75}
]

expensive=heapq.nlargest(2,portfolio,key=lambda x:x['price'])


nums=[1,6,3,6,23,9,48,-10,-5]
import heapq
heap=list(nums)
heapq.heapify(heap)
print heap

print heapq.heappop(heap)
print heapq.heappop(heap)
print heapq.heappush(heap,100)
print heap



'''
you want to implement a queue that sorts items by 
a given priority and always returns the item with 
the highest priority on each pop operation.
'''
import heapq
class PriorityQueue:
    def __init__(self):
        self._queue=[]
        self._index=0
    
    def push(self,item,priority):
        heapq.heappush(self._queue,(-priority,self._index,item))
        self._index+=1
    
    def pop(self):
        return heapq.heappop(self._queue)[-1]
    
class Item:
    def __init__(self,name):
        self.name=name
    def __repr__(self):
        return 'Item({!r})'.format(self.name) #notice the format of the expression

q=PriorityQueue()
q.push(Item('foo'),1)
q.push(Item('bar'),5)
q.push(Item('spam'),4)
q.push(Item('grok'),1)

print q.pop()
print q.pop()
print q.pop()
print q.pop()


'''
A feature of defaultdict is that it automatically
initializes the first value so you can simply focus 
on adding items.without worrying about whether the key is in the
dict or not.
'''

from collections import defaultdict

d=defaultdict(list)
d['a'].append(1)
d['b'].append(2)
d['c'].append(3)
print d

d=defaultdict(set)
d['a'].add(1)
d['b'].add(2)
d['c'].add(3)
print d


'''
to control the order of items in a dictionay,you can use an OrderedDict

An OrderedDict internally maintains a doubly linked list that orders
the keys according to insertion order.
'''
from collections import OrderedDict

d=OrderedDict()
d['foo']=1
d['bar']=2
d['spam']=3
d['grok']=4

for key in d:
    print key,d[key]
    
import json
js=json.dumps(d)
print js


#calculating with dictionaries
price={
        'acme':45.23,
        'aapl':612.78,
        'ibm':205.55,
        'hpq':37.20,
        'fb':10.75
        }

min_price=min(zip(price.values(),price.keys()))
max_price=max(zip(price.values(),price.keys()))

prices_sorted=sorted(zip(price.values(),price.keys()))

print min(price,key=lambda k:price[k])


#naming a slice

record='01357412357968461654641067968973584'
SHARES=slice(3,6)
PRICE=slice(10,12)
cost=int(record[SHARES])*float(record[PRICE])



#Determing the most frequency occurring items in a sequence

words=['look','into','my','eyes','look','into',
       'the','eyes','around','the','the','under']

from collections import Counter
word_counts=Counter(words)
top_two=word_counts.most_common(2)
print top_two
print word_counts['eyes']

morewords=['the','why','are','you','not','looking','in','my']

a=Counter(words)
b=Counter(morewords)
c=a+b
d=a-b
print c
print d


#transforming and reducing data at the same time
nums=range(1,6)
s=sum(x*x for x in nums)

import os
files=os.listdir('dirname')
if any(name.endswith('.py') for name in files):
    print 'there is python!'
else:
    print 'sorry,no python.'





