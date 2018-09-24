# -*-coding: utf-8 -*-
# Python 3.6
# Author:Zhang Haitao
# Email:13163385579@163.com
# TIME:2018-09-18  11:56
# NAME:zht-task1-trading_system.py

import time
import random
import pandas as pd
import os
import copy

DIR=r'E:\a\trading_system'

CEILING=10
FLOOR=5

random.seed(0)  #fixme:

'''
该程序模拟了股票价格的撮合过程：
1. 程序会随机(均匀分布)生成四种订单: 市价买单，市价卖单，限价买单，限价卖单 (报价限制在5-10)
2. 如果生成的是市价买单，直接与订单簿中的限价卖单成交；如果生成的是市价卖单，直接与订单簿中的限价买单成交；
如果生成的是限价买单，则将其存入bid side 订单簿，如果生产的是限价卖单，则将其存入ask side 订单簿。
3. 每次有最新的交易生成，程序会打印出最新的成交量加权成交价
'''


class Order:
    def __init__(self,time,num,side,order_type,price=None):
        self.time=time
        self.num=num
        self.side=side
        self.order_type=order_type
        self.price=price
        self.is_valid()

    @classmethod
    def random_order(cls,floor=None,ceiling=None):
        t=time.time()
        num=random.randint(1,100)*100
        if floor is None:
            floor=FLOOR
        if ceiling is None:
            ceiling=CEILING
        p = round(random.uniform(floor, ceiling), 2)
        side='bid' if random.choice([-1,1])==1 else 'ask'
        order_type= 'market' if random.choice([-1,-1,-1,1])==1 else 'limit' #trick: generate more limit order than market order
        if order_type=='market':
            p=None
        #TODO: market order should be smaller
        return cls(t,num,side,order_type,p)

    def is_valid(self):
        if self.price is not None:
            if self.price<=0:
                raise ValueError(f'Negative price is not allowed! The price is {self.price}')
        if self.num<=0:
            raise ValueError(f'Negative order number is not allowed! The order number is {self.num}')


class Market_order(Order):
    def __init__(self,time,num,side):
        super().__init__(time,num,side,'market')
        self.is_valid()

    def is_valid(self):
        if self.num<=0:
            raise ValueError(f'Negative order number is not allowed! The order number is {self.num}')


class Limit_order(Order):
    def __init__(self, time,num,side,price):
        super().__init__(time,num,side,order_type='limit',price=price)
        self.is_valid()

    def is_valid(self):
        '''
        make sure the price is positive
        '''
        if self.price<=0:
            raise ValueError(f'Negative price is not allowed! The price is {self.price}')
        if self.num<=0:
            raise ValueError(f'Negative order number is not allowed! The order number is {self.num}')


class Sell_limit_order(Limit_order):
    def __init__(self,num,ask_price):
    # def __init__(self,ask_price,num):
        t=time.time()
        super().__init__(t,num,side='ask',price=ask_price)


class Buy_limit_order(Limit_order):
    def __init__(self,num,bid_price):
        t=time.time()
        super().__init__(t,num,side='bid',price=bid_price)


class Sell_market_order(Market_order):
    def __init__(self,num):
        t=time.time()
        super().__init__(t,num,side='ask')


class Buy_market_order(Market_order):
    def __init__(self,num):
        t=time.time()
        super().__init__(t,num,side='bid')


class Orderbook:
    def __init__(self,side):
        self.side=side
        self.limit_orders=[]

    def add_new_order(self,limit_order):
        self.limit_orders.append(limit_order)
        self.sort_orders()

    def sort_orders(self):
        reverse=True if self.side=='bid' else False
        self.limit_orders=sorted(self.limit_orders, key=lambda x:(x.price, -x.time),reverse=reverse)

    def generate_random_orders(self,times=1000):
        for i in range(times):
            self.limit_orders.append(Limit_order.random_order())
        self.sort_orders()

    def remove_order(self,order):
        self.limit_orders.remove(order)


    def is_empty(self):
        return len(self.limit_orders) == 0

    @property
    def size(self):
        return len(self.limit_orders)


class Ask_orderbook(Orderbook):
    def __init__(self):
        super().__init__('ask')


class Sell_orderbook(Orderbook):
    def __init__(self):
        super().__init__('bid')


class Trading_system:
    def __init__(self):
        self.ask_ob=Ask_orderbook()
        self.bid_ob=Sell_orderbook()
        self.close_price=[]

    def simulate(self,n=10000,snapshot=False):
        for i in range(n):
            order=Order.random_order()
            self.deal(order)
            if snapshot:
                if i>0 and i%1000==0:
                    self.take_snapshot(i)
        # pd.Series(self.close_price).plot().get_figure().show()

    def take_snapshot(self,snapname):
        df_ask=pd.DataFrame([[od.time,od.num,od.side,od.order_type,od.price] for od in self.ask_ob.limit_orders],
                            columns=['time','num','side','order_type','price'])
        df_bid=pd.DataFrame([[od.time,od.num,od.side,od.order_type,od.price] for od in self.bid_ob.limit_orders],
                            columns=['time','num','side','order_type','price'])
        # df_ask.to_csv(os.path.join(DIR,f'{snapname}-ask.csv'))
        # df_bid.to_csv(os.path.join(DIR,f'{snapname}-bid.csv'))

    # TODO: mid-price
    # TODO:the price of random generated buy limit order should be smaller than mid-price
    def deal(self,order):
        if order.side=='bid':
            if self.ask_ob.is_empty():
                if order.order_type=='market':
                    pass
                elif order.order_type=='limit':
                    self.bid_ob.add_new_order(order)
            else:
                if order.order_type=='market':
                    matched=[]
                    lo=copy.copy(self.ask_ob.limit_orders)
                    #fixme: self.ask_ob may be empty
                    for head in lo:
                        self.ask_ob.remove_order(head)
                        if order.num>head.num:
                            matched.append(head)
                            order.num-=head.num
                        elif order.num==head.num:
                            matched.append(head)
                            break
                        else:
                            #fixme: check whether the value in copied object also has been changed
                            head.num=head.num-order.num
                            splitted_order=copy.copy(head)
                            splitted_order.num=order.num
                            matched.append(splitted_order)
                            if head.num>0:
                                self.ask_ob.add_new_order(head)
                            break
                    self.close_price.append(self.calculate_avg(matched))
                    print(self.calculate_avg(matched))

                elif order.order_type=='limit':
                    if order.price<self.ask_ob.limit_orders[0].price:#FIXME: mid-price
                        self.bid_ob.add_new_order(order)
                    else:
                        pass
                        # print('Invalid bid limit order')

        elif order.side=='ask':
            if self.bid_ob.is_empty():
                if order.order_type=='market':
                    pass
                elif order.order_type=='limit':
                    self.bid_ob.add_new_order(order)
            else:
                if order.order_type=='market':
                    matched=[]
                    lo=copy.copy(self.bid_ob.limit_orders)
                    for head in lo: #trick:revert the order book list
                        self.bid_ob.remove_order(head)
                        if order.num>head.num:
                            matched.append(head)
                            order.num-=head.num
                        elif order.num==head.num:
                            matched.append(head)
                            break
                        else:
                            head.num=head.num-order.num
                            splitted_order=copy.copy(head)
                            splitted_order.num=order.num
                            matched.append(splitted_order)
                            if head.num>0:
                                self.bid_ob.add_new_order(head)
                            break
                    self.close_price.append(self.calculate_avg(matched))
                    print(self.calculate_avg(matched))

                elif order.order_type=='limit':
                    if order.price>self.bid_ob.limit_orders[0].price:
                        self.ask_ob.add_new_order(order)
                    else:
                        # print('Invalid ask limit order')
                        pass

    def calculate_avg(self,matched):
        avg=sum(m.price*m.num for m in matched)/sum(m.num for m in matched)
        return avg


def statistic():
    orders=[]
    for i in range(1000):
        orders.append(Order.random_order())
    df = pd.DataFrame([[od.time, od.num, od.side, od.order_type, od.price] for od in orders],
                          columns=['time', 'num', 'side', 'order_type', 'price'])
    return df

def main():
    Trading_system().simulate(snapshot=True)


if __name__ == '__main__':
    main()








