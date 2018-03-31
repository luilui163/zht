# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 13:30:45 2016

@author: hp
"""

#Rounding numerical values
round(1.23,1) #1.2
round(1.27,1) #1.3
round(-1.27,1) #-1.3

round(1236436,-2) #1236400


#Performing accurate decimal calculations
a=4.2
b=2.1
print a+b==6.3 #False

from decimal import Decimal
a=Decimal('4.2')
b=Decimal('2.1')
print (a+b)==Decimal('6.3')


nums=[1.23e+18,1,-1.23e+18]
print sum(nums) #0.0

import math
print math.fsum(nums) #1.0


#Working with binary,octal,and hexadecimal integers
x=1234
print bin(x)
print oct(x)
print hex(x)

format(x,'b')
format(x,'o')
format(x,'x')


#Working with infinity an NaNs
a=float('inf')
b=float('-inf')
c=float('nan')
print a,b,c

import math
math.isinf(b)
math.isnan(c)
'''
NaN values propagate through all operations without raising 
an exception.

A subtle feature of NaN is that they never compare as equal.
'''


########################### The differences between array and matrix in numpy ############################
'''
Numpy matrices are strictly 2-dimensional, while numpy arrays (ndarrays) are N-dimensional. Matrix objects are a subclass of ndarray, so they inherit all the attributes and methods of ndarrays.
The main advantage of numpy matrices is that they provide a convenient notation for matrix multiplication: if a and b are matrices, then a*b is their matrix product.
'''
import numpy as np

a=np.mat('4 3; 2 1')
b=np.mat('1 2; 3 4')
print(a)
# [[4 3]
#  [2 1]]
print(b)
# [[1 2]
#  [3 4]]
print(a*b)
# [[13 20]
#  [ 5  8]]
'''
Both matrix objects and ndarrays have .T to return the transpose, but matrix objects also have .H for the conjugate transpose, and .I for the inverse.
In contrast, numpy arrays consistently abide by the rule that operations are applied element-wise. Thus, if a and b are numpy arrays, then a*b is the array formed by multiplying the components element-wise:
'''
c=np.array([[4, 3], [2, 1]])
d=np.array([[1, 2], [3, 4]])
print(c*d)
# [[4 6]
#  [6 4]]
'''
To obtain the result of matrix multiplication, you use np.dot :
'''
print(np.dot(c,d))
# [[13 20]
#  [ 5  8]]
'''
The ** operator also behaves differently:
'''
print(a**2)
# [[22 15]
#  [10  7]]
print(c**2)
# [[16  9]
#  [ 4  1]]
'''
Since a is a matrix, a**2 returns the matrix product a*a. Since c is an ndarray, c**2 returns an ndarray with each component squared element-wise.
There are other technical differences between matrix objects and ndarrays (having to do with np.ravel, item selection and sequence behavior).
The main advantage of numpy arrays is that they are more general than 2-dimensional matrices. What happens when you want a 3-dimensional array? Then you have to use an ndarray, not a matrix object. Thus, learning to use matrix objects is more work -- you have to learn matrix object operations, and ndarray operations.
Writing a program that uses both matrices and arrays makes your life difficult because you have to keep track of what type of object your variables are, lest multiplication return something you don't expect.
In contrast, if you stick solely with ndarrays, then you can do everything matrix objects can do, and more, except with slightly different functions/notation.
If you are willing to give up the visual appeal of numpy matrix product notation, then I think numpy arrays are definitely the way to go.
PS. Of course, you really don't have to choose one at the expense of the other, since np.asmatrix and np.asarray allow you to convert one to the other (as long as the array is 2-dimensional).
'''


#Picking things at random
import random
values=range(1,7)
random.choice(values)
random.sample(values,3)
random.shuffle(values)

random.randint(0,10) #o,and 10 are included

'''
To get N random-bits expressed as an integer,use random.getrandbits()
'''
random.getrandbits(200)


#Converting days to seconds,and other basic time conversions
import datetime

a=datetime.timedelta(days=2,hours=6)
b=datetime.timedelta(hours=4.5)
c=a+b
c.days
c.seconds #37800
c.seconds/3600.0 #10.5
c.total_seconds()/3600.0 #58.5

a=datetime.datetime(2012,9,23)
print a+datetime.timedelta(days=10)

b=datetime.datetime(2012,12,21)
d=b-a
print d.days

now=datetime.datetime.today()
print now

print now+datetime.timedelta(minutes=10)

#Converting strings into datetimes
from datetime import datetime
text='2012-09-20'
y=datetime.strptime(text,'%Y-%m-%d')
z=datetime.now()
diff=z-y
diff #datetime.timedelta(1452, 62580, 831000)

nice_z=datetime.strftime(z,'%A %B %d, %Y')
nice_z #'Sunday September 11, 2016'

def parse_ymd(s):
    year_s,mon_s,day_s=s.split('-')
    return datetime(int(year_s),int(mon_s),int(day_s))
    



















