# -*- coding: utf-8 -*-
"""
Created on Sat May 28 10:34:41 2016

@author: Administrator
"""

class Moveable:
    def move(self):
        print 'moveable...'

class MoveOnFeet(Moveable):
    def move(self):
        print 'move on feet.'

class MoveOnWheels(Moveable):
    def move(self):
        print 'move on wheels.'

class MoveObj:
    def set_move(self,moveable):
        self.moveable=moveable()
    
    def move(self):
        self.moveable.move()
        
class Test:
    def move(self):
        print "I'm flying."


if __name__=='__main__':
    m=MoveObj()
    m.set_move(Moveable)
    m.move()
    m.set_move(MoveOnFeet)
    m.move()
    m.set_move(MoveOnWheels)
    m.move()
    m.set_move(Test)
    m.move()