#-*-coding: utf-8 -*-
#author:tyhj
#listu.py 2017/9/8 21:57

def chunkify(lst,n):
    '''
    splitting a list into N parts of approximately equal length
    refer to:https://stackoverflow.com/questions/2130016/splitting-a-list-of-into-n-parts-of-approximately-equal-length

    example:
        >> chunkify( range(13), 3)
        [[0, 3, 6, 9, 12], [1, 4, 7, 10], [2, 5, 8, 11]]

    Args:
        lst:list
        n:

    Returns:

    '''
    return [lst[i::n] for i in xrange(n)]


def chunkifyByBreakPoints(lst,breakPoints):
    '''
    splitting a list into N parts according the breakPoints

    examples:
    >>chunkifyByBeakPoints(range(15),[0.3,0.7])
      [[0, 1, 2, 3], [4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14]]

    Args:
        lst:
        breadPoints: list

    Returns:

    '''
    ns=[0]
    ns+=[int(point*len(lst)) for point in breakPoints]
    ns+=[len(lst)]
    sublist=[lst[ns[i-1]:ns[i]] for i in range(1,len(ns))]
    return sublist












