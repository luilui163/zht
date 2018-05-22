# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-05-22  15:12
# NAME:xiangqi-sp.py

import database_api as dpi


oper_rev=dpi.get_stocks_data('equity_selected_income_sheet_q',['oper_rev'],
                             '2004-01-01', '2018-03-01')

cap=dpi.get_stocks_data('')







