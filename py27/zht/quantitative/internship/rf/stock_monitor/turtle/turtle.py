#-*-coding: utf-8 -*-
#@author:tyhj

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

'''
说明：
1，T中存储的cash,float profit等是在已经交易了T出现的信号之后的状态，T中存储的signal是T时刻要交易的signal。
2，都是市价单
3,cash 标示的是在买入或卖出之后的现金，如果要知道T时刻可用的现金，应该看T-1的值
'''

class Underlying:
    def __init__(self,code,margin_rate,minimum_units,multiplier):
        self.code=code
        self.margin_rate=margin_rate
        self.minimum_units=minimum_units
        self.multiplier=multiplier

class Commission:
    def __init__(self,code,mode,value):
        self.code=code
        self.mode=mode
        self.value=value

class Slippage:
    def __init__(self,mode,value):
        self.mode=mode
        self.value=value

class Turtle:
    def __init__(self,code,df,window,underlying,initial_value,commission,slippage):
        self.code=code
        self.df=df
        self.window=window
        self.underlying=underlying
        self.initial_value=initial_value
        self.commission=commission
        self.slippage=slippage

        self.df['band_up']=self.df['high'].rolling(self.window).max().shift(1)
        self.df['band_down']=self.df['low'].rolling(self.window).min().shift(1)
        self.calculate_N()
        self.df=self.df[50:]#delete some rows to avoid NaN values
        self.last_deal_price=0.0
        self.df['units']=0.0
        self.df['position']=0.0
        self.df['position'][0]=0.0
        self.df['signal_in'] = np.NaN
        self.df['cash']=0.0
        self.df['cash'][0]=initial_value
        self.df['float_capital'] = 0.0
        self.df['float_capital'][0]=initial_value
        self.df['commission']=0.0
        self.df['add']=np.NaN
        self.df['stop_loss']=np.NaN
        self.df['stop_profit']=np.NaN

    def check_position(self,i):
        if self.df['position'][i-1]>0:
            return 1
        elif self.df['position'][i-1]<0:
            return -1 #short
        else:
            return 0

    def calculate_N(self):
        self.df['true_range']=np.NaN
        self.df['N']=np.NaN
        for i in range(1,len(self.df)):
            a1=self.df['high'][i]-self.df['low'][i]
            a2=self.df['high'][i]-self.df['close'][i-1]
            a3=self.df['close'][i-1]-self.df['low'][i]
            self.df['true_range'][i]=max(a1,a2,a3)
        self.df['N']=self.df['true_range'].rolling(20).mean()

    def calculate_trading_position(self,i):
        if self.commission.mode==1:
            x=(self.df['cash'][i-1]*0.01)/(self.df['N'][i]*self.underlying.multiplier*(1+self.slippage+self.commission.value))#note:the index for cash should be i-1
        elif self.commission.mode==2:
            x=(self.df['cash'][i-1]*0.01)/(self.df['N'][i]*self.underlying.multiplier+self.slippage+self.commission.value/100.0)
        x=int(x/100)*100
        return x #the number of underlying to trade

    def signal_in(self,i):
        if self.check_position(i)==0 and self.df['close'][i]>self.df['band_up'][i]:
            self.last_deal_price=self.df['close'][i]
            return 1
        else:
            return 0

    def add(self,i):
        if self.check_position(i)==1 and self.df['close'][i]>(self.last_deal_price+0.5*self.df['N'][i]):
            self.last_deal_price=self.df['close'][i]
            return 1
        else:
            return 0

    def stop_loss(self,i):
        if self.check_position(i)==1 and self.df['close'][i]<(self.last_deal_price-2*self.df['N'][i]):
            return 1
        else:
            return 0

    def stop_profit(self,i):
        if self.check_position(i)==1 and self.df['close'][i]<self.df['band_down'][i]:
            return 1
        else:
            return 0

    #Is commission rate the same for both side? Suppose them as the same in this backtest system.
    def calculate_commission(self,i):
        if self.commission.mode==1:#perValue
            x=self.calculate_trading_position(i)*self.underlying.multiplier*self.df['close'][i]*self.commission.value
            return x
        elif self.commission.mode==2:#perShare
            x=self.calculate_trading_position(i)/100*self.commission.value
            return x

    def backtest(self):
        for i in range(1, len(self.df)):
            self.df['cash'][i] =self.df['cash'][i-1]
            self.df['units'][i]=self.df['units'][i-1]
            self.df['position'][i]=self.df['position'][i-1]
            self.df['float_capital'][i]=self.df['float_capital'][i-1]

            if self.signal_in(i) == 1:
                self.df['cash'][i] -= self.calculate_trading_position(
                    i) * self.underlying.multiplier * self.df['close'][i] - self.calculate_commission(i)
                self.df['commission'][i] += self.calculate_commission(i)
                self.df['position'][i] += self.calculate_trading_position(i)
                self.df['units'][i] += 1
                self.df['signal_in'][i] = 1

            if self.add(i) == 1:
                self.df['cash'][i] -= self.calculate_trading_position(i) * self.underlying.multiplier * self.df['close'][
                    i] - self.calculate_commission(i)
                self.df['commission'][i] += self.calculate_commission(i)
                self.df['position'][i] += self.calculate_trading_position(i)
                self.df['units'][i] += 1
                self.df['add'][i]=1

            if self.stop_loss(i) == 1:
                self.df['cash'][i] += self.df['position'][i] * self.df['close'][
                    i] * self.underlying.multiplier - self.calculate_commission(i)
                self.df['commission'][i] += self.calculate_commission(i)
                self.df['position'][i] = 0
                self.df['units'][i] = 0
                self.df['stop_loss'][i]=1

            if self.stop_profit(i) == 1:
                self.df['cash'][i] += self.df['position'][i] * self.df['close'][
                    i] * self.underlying.multiplier - self.calculate_commission(i)
                self.df['commission'][i] += self.calculate_commission(i)
                self.df['position'][i] = 0
                self.df['units'][i] = 0
                self.df['stop_profit'][i]=1

            self.df['float_capital'][i] = self.df['cash'][i] + self.df['position'][i] * self.df['close'][
                i] * self.underlying.multiplier

            print 'backtesting date %s...'%df.index[i]
        print 'backtesting finished!'

    def calculate_performance(self):
        self.df['net_value']=self.df['float_capital']/self.initial_value
        self.performance={}
        self.performance['win_rate']=self.win_rate()
        self.performance['pnl_ratio']=self.pnl_ratio()
        self.performance['return_per_year']=self.return_per_year()
        self.performance['max_drawdown'],self.performance['max_drawdown_duration']=self.drawdown()

    def save_performance(self):
        df=self.df[['cash','float_capital','net_value']]
        df.to_csv('%s.csv'%self.code)
        with open('%s.txt'%self.code,'w') as f:
            f.write('win rate\t%f\n'%self.performance['win_rate'])
            f.write('profit and loss ratio\t%f\n'%self.performance['pnl_ratio'])
            f.write('annual return\t%f\n'%self.performance['return_per_year'])
            f.write('max drawdown\t%f\n'%self.performance['max_drawdown'])
            f.write('max drawdown duration\t%d days\n'%int(self.performance['max_drawdown_duration']))
        fig=plt.figure()
        self.df['net_value'].plot()
        fig.savefig('%s.png'%self.code)

    def win_rate(self):
        #exactly,this is not win rate
        a=self.df['float_capital']-self.df['float_capital'].shift(1)
        positive=a[a>0].count()
        negative=a[a<0].count()
        return positive*1.0/(positive+negative)

    def pnl_ratio(self):
        pnl=self.df['float_capital']-self.df['float_capital'].shift(1)
        avg_profit=pnl[pnl>0].mean()
        avg_loss=pnl[pnl<0].mean()
        return avg_profit/abs(avg_loss)

    def return_per_year(self):
        a=(self.df['net_value'][-1]-1)/len(self.df)*252
        return a

    def drawdown(self):
        hwm=[0]
        drawdown=pd.Series(index=self.df.index)
        duration=pd.Series(index=self.df.index)

        for i in range(1,len(self.df)):
            hwm.append(max(hwm[i-1],self.df['net_value'][i]))
            drawdown[i]=hwm[i]-self.df['net_value'][i]
            duration[i]=(0 if drawdown[i]==0 else duration[i-1]+1)
        return drawdown.max(),duration.max()

    def run(self):
        self.backtest()
        self.calculate_performance()
        self.save_performance()


if __name__=='__main__':
    window=10
    slippage=0
    cwd=os.getcwd()
    commission_df=pd.read_csv(os.path.join(cwd,'commission.csv'),index_col=0)
    dirpath=os.path.join(cwd,'data')
    filenames=os.listdir(dirpath)
    for filename in filenames[26:]:
        code=filename.upper().split('_')[0]
        print code
        df=pd.read_csv(os.path.join(dirpath,filename),index_col=0)
        index=df.index
        df.index = [pd.Timestamp(nd) for nd in df.index]
        commission=Commission(code,mode=commission_df.loc[code,'mode'],value=commission_df.loc[code,'value'])
        underlying = Underlying(code, margin_rate=0.09, minimum_units=1, multiplier=commission_df.loc[code,'multiplier'])
        test = Turtle(code, df, window, underlying, 100000000, commission, slippage)
        test.run()
        print filename





















