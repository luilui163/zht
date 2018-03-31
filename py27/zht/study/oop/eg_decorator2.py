# -*- coding: utf-8 -*-
"""
Created on Sat May 28 15:10:01 2016

@author: Administrator
"""

def deco(a_class):
    class Newclass:
        def __init__(self,age,color):
            self.wrapped=a_class(age)
            self.color=color
        
        def display(self):
            print self.color
            print self.wrapped.age
    
    return Newclass

@deco
class Cat:
    def __init__(self,age):
        self.age=age
    
    def display(self):
        print self.age
    

if __name__=='__main__':
    c=Cat(12,'Black')
    c.display()