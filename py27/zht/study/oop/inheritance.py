# -*- coding: utf-8 -*-
"""
Created on Thu May 26 19:47:49 2016

@author: Administrator
"""
class Point(object):##注意后边要继承的话，这里一定不能少了object，这一点与python3.x不同
    def __init__(self,x,y):
        self.x=x
        self.y=y
    
    def __add__(self,oth):
        return Point(self.x+oth.x,self.y+oth.y)
    
    def info(self):
        print self.x,self.y

class D3Point(Point):
    def __init__(self,x,y,z):
#        super(D3Point,self).__init__(x,y)
        super(D3Point,self).__init__(x,y) 
        self.z=z
    
    def __add__(self,oth):
        return D3Point(self.x+oth.x,self.y+oth.y,self.z+oth.z)
    
    def info(self):
        print self.x,self.y,self.z


def myadd(a,b):
    return a+b

if __name__=='__main__':
    myadd(Point(1,2),Point(3,4)).info()
    myadd(D3Point(1,2,3),D3Point(3,5,2)).info()


