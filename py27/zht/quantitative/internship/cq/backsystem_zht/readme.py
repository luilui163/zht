# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 14:42:35 2016

@author: hp
"""

'''
1,DATA:

data.txt:
    sid    date   v1    v2    ...    
    sid    date   v1    v2    ...    
    sid    date   v1    v2    ...    
    sid    date   v1    v2    ...    
    sid    date   v1    v2    ...    
    sid    date   v1    v2    ...    
    sid    date   v1    v2    ...    
    sid    date   v1    v2    ...    
    ...



data_description.txt:
    variable1    col_number    'c'
    variable2    col_number    'd'
    ...

variable/
    d/
        discrete_variable1.txt:
                value1    '1'    number
                value2    '2'    number
                ...
        discrete_variable2.txt
        ...
    c/
        continuous_variable1.txt:
                interval1
                interval2
                ...
        continuous_variable2.txt
        ...


2,CHOOSE STOCK:

(1)compare values in one variable:




(2)cross conditions
condition1:
    variable    'c' or 'd'    specific_value
condition2:
    variable    'c' or 'd'    specific_value



3.GET RESULT:
(1)compare values in one variable:
fig/
    variable.png
    variable_description.txt:
        value1    IR    win_rate
        value2    IR    win_rate


(2)cross conditions
fig/
    condition1_condition2.png
    condition1_condition2_description.txt:
        IR
        win_rate
        condition1
        condition2
        ....
        
    condition1_condition2.png
    condition1_condition2_description.txt:
        IR
        win_rate
        condition1
        condition2
        ....
        
    condition1_condition2.png
    condition1_condition2_description.txt:
        IR
        win_rate
        condition1
        condition2
        ....
    
'''