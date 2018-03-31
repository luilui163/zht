# -*-coding: utf-8 -*-
# author:tyhj
# regressionModels.py 2017/9/10 10:24
import pandas as pd
import os
import numpy as np
import time
import itertools
import uuid
from shutil import copyfile

from zht.util import pandasu
from zht.util.statu import GRS_test
from zht.util.mathu import getSortedPortId
from zht.util.listu import chunkify

from params import *
from main import get_portRet


def multiTest():
    cwd=os.getcwd()
    command='python %s'%(os.path.join(cwd,'a.py'))
    os.system(command)

# multiTest()

scriptPath=os.path.join(os.getcwd(),'a.py')



