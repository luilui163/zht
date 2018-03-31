#-*-coding: utf-8 -*-
#@author:tyhj

import beta_hsigma
import momentum
import volatility
import normalize_the_factors

def start():
    beta_hsigma.run()
    momentum.run()
    volatility.run()
    normalize_the_factors.run()



if __name__=='__main__':
    start()











