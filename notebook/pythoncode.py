
import numpy as np
def append_if_not_exists(arr,x):
    if x not in arr:
    arr.append(x)

def some_useless_slow_function():
    arr=list()
    for x in range(10000):
        x=np.random.randint(0,10000)
        append_if_not_exists(arr,x)