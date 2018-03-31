# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 14:52:58 2016

@author: Administrator
"""
import numpy as np
import math
import seaborn as sns
from matplotlib import pylab

ttm = 3.0
tSteps = 25
r = 0.03
d = 0.02
sigma = 0.2
strike = 100.0
spot = 100.0


# 二叉树框架（可以通过传入不同的treeTraits类型，设计不同的二叉树结构）
class BinomialTree:
    def __init__(self, spot, riskFree, dividend, tSteps, maturity, sigma, treeTraits):
        self.dt = maturity / tSteps
        self.spot = spot
        self.r = riskFree
        self.d = dividend
        self.tSteps = tSteps
        self.discount = math.exp(-self.r*self.dt)
        self.v = sigma
        self.up = treeTraits.up(self)
        self.down = treeTraits.down(self)
        self.upProbability = treeTraits.upProbability(self)
        self.downProbability = 1.0 - self.upProbability
        self._build_lattice()
        
    def _build_lattice(self):
        '''
        完成构造二叉树的工作
        '''
        self.lattice = np.zeros((self.tSteps+1, self.tSteps+1))
        self.lattice[0][0] = self.spot
        for i in range(self.tSteps):
            for j in range(i+1):
                self.lattice[i+1][j+1] = self.up * self.lattice[i][j]
            self.lattice[i+1][0] = self.down * self.lattice[i][0]
            
    def roll_back(self, payOff):
        '''
        节点计算，并反向倒推
        '''
        for i in range(self.tSteps,0,-1):
            for j in range(i,0,-1):
                if i == self.tSteps:
                    self.lattice[i-1][j-1] = self.discount * (self.upProbability * payOff(self.lattice[i][j]) + self.downProbability * payOff(self.lattice[i][j-1]))
                else:
                    self.lattice[i-1][j-1] = self.discount * (self.upProbability *  self.lattice[i][j] + self.downProbability * self.lattice[i][j-1])
                    

class JarrowRuddTraits:
    @staticmethod
    def up(tree):
        return math.exp((tree.r - tree.d - 0.5*tree.v*tree.v)*tree.dt + tree.v*math.sqrt(tree.dt))
    
    @staticmethod
    def down(tree):
        return math.exp((tree.r - tree.d - 0.5*tree.v*tree.v)*tree.dt - tree.v*math.sqrt(tree.dt))
    
    @staticmethod
    def upProbability(tree):
        return 0.5

class CRRTraits:  
    @staticmethod
    def up(tree):
        return math.exp(tree.v * math.sqrt(tree.dt))
    
    @staticmethod
    def down(tree):
        return math.exp(-tree.v * math.sqrt(tree.dt))
    
    @staticmethod
    def upProbability(tree):
        return 0.5 + 0.5 * (tree.r - tree.d - 0.5 * tree.v*tree.v) * tree.dt / tree.v / math.sqrt(tree.dt)



def pay_off(spot):
    global strike
    return max(spot - strike, 0.0)



testTree = BinomialTree(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits)
testTree.roll_back(pay_off)
print u'二叉树价格： %.4f' % testTree.lattice[0][0]




stepSizes = range(25, 500,25)
jrRes = []
crrRes = []
for tSteps in stepSizes:
    # Jarrow - Rudd 结果
    testTree = BinomialTree(spot, r, d, tSteps, ttm, sigma, JarrowRuddTraits)
    testTree.roll_back(pay_off)
    jrRes.append(testTree.lattice[0][0])
    
    # Cox - Ross - Rubinstein 结果
    testTree = BinomialTree(spot, r, d, tSteps, ttm, sigma, CRRTraits)
    testTree.roll_back(pay_off)
    crrRes.append(testTree.lattice[0][0])



#anyRes = [BSMPrice(1, strike, spot, r, d, sigma, ttm, rawOutput= True)[0]] * len(stepSizes)

pylab.figure(figsize = (16,8))
pylab.plot(stepSizes, jrRes, '-.', marker = 'o', markersize = 10)
pylab.plot(stepSizes, crrRes, '-.', marker = 'd', markersize = 10)
#pylab.plot(stepSizes, anyRes, '--')
pylab.legend(['Jarrow - Rudd', 'Cox - Ross - Rubinstein', u'解析解'], prop = font)
pylab.xlabel(u'二叉树步数', fontproperties = font)
pylab.title(u'二叉树算法收敛性测试', fontproperties = font, fontsize = 20)






























































                    