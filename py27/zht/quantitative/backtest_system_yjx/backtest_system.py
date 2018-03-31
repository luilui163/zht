#-*- coding=utf-8 -*-
import pandas as pd
import numpy as np
import os
import datetime
from pandas.tseries.offsets import BDay
import matplotlib.pyplot as plt
import re


class config(object):
    def __init__(self, path, holding_day, test_window):
        self.path = path
        self.holding_day = holding_day
        self.test_window = test_window
        self.pathdir = os.listdir(path)
        self.dataset_weight1 = {}
        self.dataset_weight2 = {}
        self.dataset = {}
        self.market_value = pd.read_csv('E:\\data\\2010_now\\market_value.csv')
        self.market_value.iloc[:, 0] = self.market_value.iloc[:, 0].astype(str)
        self.market_value = self.market_value.set_index('date')
        self.stock_data_return = pd.read_csv('E:\\data\\2010_now\\close_pct.csv')
        self.stock_data_return.iloc[:, 0] = self.stock_data_return.iloc[:, 0].astype(str)
        self.stock_data_return = self.stock_data_return.set_index('date')
        self.market_volume = pd.read_csv('E:\\data\\2010_now\\volume.csv')
        self.market_volume.iloc[:, 0] = self.market_volume.iloc[:, 0].astype(str)
        self.market_volume = self.market_volume.set_index('date')
        self.data_return = pd.DataFrame(index=self.stock_data_return.index)
        self.dataset_weight1_table = pd.DataFrame(index=self.stock_data_return.index)
        self.dataset_weight2_table = pd.DataFrame(index=self.stock_data_return.index)
        self.dataset_weight_table = pd.DataFrame(index=self.stock_data_return.index)
        self.data_sum = pd.DataFrame(index=self.stock_data_return.index)

class stock_signal(config):
    def raw_data_process_get_signal(self):
        for every_path in self.pathdir:
            self.announced_time=str(every_path[0:-4])
            for each_line in open(self.path + every_path):
                self.data = each_line.strip().split(',')
                if len(self.data) > 5 and (self.data[0][-2:] == 'SZ' or self.data[0][-2:] == 'SS') and self.data[3] != '':
                    self.name = self.data[0]
                    self.happen_date = self.data[-2]
                    self.state = self.data[4]
                    self.last = self.data[5]
                    self.num = self.data[3]
                    self.num_Data = self.num.strip().split('|')
                    self.test_date=self.data[-1]
                    if len(self.num_Data) == 2:
                        self.num1 = float(self.num_Data[0][0:-1]) / 100.0
                        self.num2 = float(self.num_Data[1][0:-1]) / 100.0
                        self.final_num = np.max([self.num1, self.num2])
                    if len(self.num_Data) == 1:
                        self.final_num = float(self.num_Data[0][0:-1]) / 100.0
                    if str(self.announced_time) == self.happen_date:
                        self.announced_time_format = datetime.datetime.strptime(self.announced_time, '%Y%m%d')
                    else:
                        self.announced_time = self.happen_date
                        self.announced_time_format = datetime.datetime.strptime(self.announced_time, '%Y%m%d')
                    self.test_announced_time_format = self.announced_time_format
                    while datetime.datetime.strftime(self.test_announced_time_format,
                                                     '%Y%m%d') not in self.stock_data_return.index:
                        self.test_announced_time_format -= BDay(1)
                    self.test_announced_time = datetime.datetime.strftime(self.test_announced_time_format, '%Y%m%d')
                    self.stop_date = (datetime.datetime.strptime(self.announced_time, '%Y%m%d') + BDay(self.holding_day)).strftime('%Y%m%d')

                    yes_market_value=self.market_value.loc[self.test_announced_time,:]
                    new_yes_market_value=yes_market_value.T


                    top_1000= float((new_yes_market_value.describe(percentiles=0.3))['30%'])


                    if int(self.stop_date) <= int(self.stock_data_return.index[-1]):
                        while str(self.stop_date) not in self.stock_data_return.index:
                            self.stop_date = datetime.datetime.strptime(self.stop_date, '%Y%m%d')
                            self.stop_date = self.stop_date + BDay(1)
                            self.stop_date = datetime.datetime.strftime(self.stop_date, '%Y%m%d')
                        self.stop_date_format = datetime.datetime.strptime(self.stop_date, '%Y%m%d')

                    if self.name in self.stock_data_return.columns and (self.state=='预增' or self.state=='预盈' ) \
                           and float(yes_market_value[self.name])<top_1000 :#and (self.test_date[-5:]=='12-31' or self.test_date[-5]=='03-31'):

                       if self.dataset_weight1.has_key(self.announced_time):
                           self.dataset_weight1[self.announced_time][self.name] = str(float(self.last))
                       else:
                           self.dataset_weight1[self.announced_time] = {}
                           self.dataset_weight1[self.announced_time][self.name] = str(float(self.last))
                       if self.dataset_weight2.has_key(self.announced_time):
                           self.dataset_weight2[self.announced_time][self.name] = str(float(self.final_num))
                       else:
                           self.dataset_weight2[self.announced_time] = {}
                           self.dataset_weight2[self.announced_time][self.name] = str(float(self.final_num))
                       if self.dataset.has_key(self.announced_time):
                           self.dataset[self.announced_time][self.name] = self.stop_date
                       else:
                           self.dataset[self.announced_time] = {}
                           self.dataset[self.announced_time][self.name] = self.stop_date
                    else:
                        pass

    def get_signal(self):
        self.raw_data_process_get_signal()
        return self.dataset, self.dataset_weight1, self.dataset_weight2

class calculation(stock_signal):
    def return_mode1(self):
        for each_day in self.dataset.keys():
            for each_stock in self.dataset[each_day].keys():
                stock_name = str(each_stock)
                self.dataset_weight1_table[stock_name] = 0.0
                if len(self.dataset_weight2)!=0:
                    self.dataset_weight2_table[stock_name] = 0.0
                self.data_return[stock_name] = 0.0
                self.dataset_weight_table[stock_name] = 0.0
        for each_day in self.dataset.keys():
            start_tem_date = (datetime.datetime.strptime(each_day, '%Y%m%d') + BDay(1))

            while datetime.datetime.strftime(start_tem_date, '%Y%m%d') not in self.stock_data_return.index:
                start_tem_date += BDay(1)
            start_tem_date = datetime.datetime.strftime(start_tem_date, '%Y%m%d')
            start_day = list(self.stock_data_return.index).index(str(start_tem_date))
            for each_stock in self.dataset[each_day].keys():
                end_day = list(self.stock_data_return.index).index(str(self.dataset[each_day][each_stock]))
                stock_name = str(each_stock)
                if self.stock_data_return[stock_name][start_day - 1:start_day].values <= 0.099 and \
                            self.stock_data_return[stock_name][start_day - 1:start_day].values >= -0.099:

                        self.data_return[stock_name][start_day:(end_day + 1)] = \
                            self.stock_data_return[stock_name][start_day:(end_day + 1)].values
                        self.dataset_weight1_table[stock_name][start_day:end_day + 1] = \
                            float(self.dataset_weight1[each_day][stock_name])
                        if len(self.dataset_weight2)!=0:
                            self.dataset_weight2_table[stock_name][start_day:end_day + 1] = \
                                float(self.dataset_weight2[each_day][stock_name])
                        else:
                            pass



        self.dataset_weight1_table = self.dataset_weight1_table.fillna(0.0)
        if len(self.dataset_weight2) != 0:
            self.dataset_weight2_table = self.dataset_weight2_table.fillna(0.0)
        else:
            pass

        self.dataset_weight_table = self.dataset_weight_table.fillna(0.0)
        self.stock_data_return = self.stock_data_return.fillna(0.0)
        self.data_return = self.data_return.fillna(0.0)
        for each in range(0, len(self.data_return.index)):
            if len(self.dataset_weight2)!=0:
                nonzero = (np.nonzero(np.asarray(self.dataset_weight1_table.iloc[each, :].values)))[0]

                tem_list1 = []
                tem_list2 = []
                if list(nonzero) == []:
                    pass
                else:
                    for i in list(nonzero):
                        tem_list1.append(self.dataset_weight1_table.iloc[each, i])
                        tem_list2.append(self.dataset_weight2_table.iloc[each, i])

                    change = np.argsort(tem_list1)
                    new_tem_list1 = []
                    new_tem_list2 = []
                    for each_1 in change:
                        new_tem_list1.append(tem_list1[each_1])
                        new_tem_list2.append(tem_list2[each_1])

                    k = 1
                    change1 = list(np.argsort(new_tem_list1))
                    new_change1 = np.zeros(len(new_tem_list1))

                    for j in change1:
                        new_change1[j] = k
                        k += 1
                    kk = 1
                    change2 = list(np.argsort(new_tem_list2))
                    new_change2 = np.zeros(len(new_tem_list2))
                    for j in change2:
                        new_change2[j] = kk
                        kk += 1

                    new_final_change = new_change1 * new_change2
                    num = float(np.sum(new_final_change))
                    final_change = new_final_change / float(num)
                    for j in range(0, len(tem_list1)):
                        self.dataset_weight_table.iloc[each, list(nonzero)[j]] = final_change[j]

            if len(self.dataset_weight2) == 0:
                nonzero = (np.nonzero(np.asarray(self.dataset_weight1_table.iloc[each, :].values)))[0]
                tem_list1 = []
                if list(nonzero) == []:
                    pass
                else:
                    for i in list(nonzero):
                        tem_list1.append(self.dataset_weight1_table.iloc[each, i])
                    change = np.argsort(tem_list1)
                    new_tem_list1 = []
                    for each_1 in change:
                        new_tem_list1.append(tem_list1[each_1])
                    k = 1
                    change1 = list(np.argsort(new_tem_list1))
                    new_change1 = np.zeros(len(new_tem_list1))
                    for j in change1:
                        new_change1[j] = k
                        k += 1
                    new_final_change = new_change1
                    num = float(np.sum(new_final_change))
                    final_change = new_final_change / float(num)
                    for j in range(0, len(tem_list1)):
                        self.dataset_weight_table.iloc[each, list(nonzero)[j]] = final_change[j]

        for i in range(0, len(self.data_return.index)):
            if np.all(self.data_return.iloc[i, :] == 0.0):
                self.stock_data_return.iloc[i, :] = 0.0
            num_ = float(np.count_nonzero(self.stock_data_return.iloc[i, :]))
            if num_ != 0.0:
                self.stock_data_return.iloc[i, :] = self.stock_data_return.iloc[i, :] / num_ * (-0.5)
        self.data_return = self.data_return * 0.5 * self.dataset_weight_table

        self.data_return['market'] = np.sum(self.stock_data_return, axis=1)
        self.data_sum['mode_1'] = np.sum(self.data_return, axis=1)
        print("IR=", self.data_sum.mean(axis=0) / self.data_sum.std(axis=0))
        print('total_return', np.sum(self.data_sum))

        np.cumsum(self.data_sum).plot()
        plt.show()

    def return_mode0(self):
        for each_day in self.dataset.keys():
            for each_stock in self.dataset[each_day].keys():
                stock_name = str(each_stock)
                self.dataset_weight1_table[stock_name] = 0.0
                if len(self.dataset_weight2) != 0:
                    self.dataset_weight2_table[stock_name] = 0.0
                self.data_return[stock_name] = 0.0
                self.dataset_weight_table[stock_name] = 0.0
        for each_day in self.dataset.keys():
            start_tem_date = (datetime.datetime.strptime(each_day, '%Y%m%d') + BDay(0))

            while datetime.datetime.strftime(start_tem_date, '%Y%m%d') not in self.stock_data_return.index:
                start_tem_date += BDay(1)
            start_tem_date = datetime.datetime.strftime(start_tem_date, '%Y%m%d')
            start_day = list(self.stock_data_return.index).index(str(start_tem_date))
            for each_stock in self.dataset[each_day].keys():
                end_day = list(self.stock_data_return.index).index(str(self.dataset[each_day][each_stock]))
                stock_name = str(each_stock)
                if self.stock_data_return[stock_name][start_day - 1:start_day].values <= 0.099 and \
                                self.stock_data_return[stock_name][start_day - 1:start_day].values >= -0.099:

                    self.data_return[stock_name][start_day:(end_day + 1)] = \
                        self.stock_data_return[stock_name][start_day:(end_day + 1)].values
                    self.dataset_weight1_table[stock_name][start_day:end_day + 1] = \
                        float(self.dataset_weight1[each_day][stock_name])
                    if len(self.dataset_weight2) != 0:
                        self.dataset_weight2_table[stock_name][start_day:end_day + 1] = \
                            float(self.dataset_weight2[each_day][stock_name])
                    else:
                        pass

        self.dataset_weight1_table = self.dataset_weight1_table.fillna(0.0)
        if len(self.dataset_weight2) != 0:
            self.dataset_weight2_table = self.dataset_weight2_table.fillna(0.0)
        else:
            pass

        self.dataset_weight_table = self.dataset_weight_table.fillna(0.0)
        self.stock_data_return = self.stock_data_return.fillna(0.0)
        self.data_return = self.data_return.fillna(0.0)
        for each in range(0, len(self.data_return.index)):
            if len(self.dataset_weight2) != 0:
                nonzero = (np.nonzero(np.asarray(self.dataset_weight1_table.iloc[each, :].values)))[0]

                tem_list1 = []
                tem_list2 = []
                if list(nonzero) == []:
                    pass
                else:
                    for i in list(nonzero):
                        tem_list1.append(self.dataset_weight1_table.iloc[each, i])
                        tem_list2.append(self.dataset_weight2_table.iloc[each, i])

                    change = np.argsort(tem_list1)
                    new_tem_list1 = []
                    new_tem_list2 = []
                    for each_1 in change:
                        new_tem_list1.append(tem_list1[each_1])
                        new_tem_list2.append(tem_list2[each_1])

                    k = 1
                    change1 = list(np.argsort(new_tem_list1))
                    new_change1 = np.zeros(len(new_tem_list1))

                    for j in change1:
                        new_change1[j] = k
                        k += 1
                    kk = 1
                    change2 = list(np.argsort(new_tem_list2))
                    new_change2 = np.zeros(len(new_tem_list2))
                    for j in change2:
                        new_change2[j] = kk
                        kk += 1

                    new_final_change = new_change1 * new_change2
                    num = float(np.sum(new_final_change))
                    final_change = new_final_change / float(num)
                    for j in range(0, len(tem_list1)):
                        self.dataset_weight_table.iloc[each, list(nonzero)[j]] = final_change[j]

            if len(self.dataset_weight2) == 0:
                nonzero = (np.nonzero(np.asarray(self.dataset_weight1_table.iloc[each, :].values)))[0]
                tem_list1 = []
                if list(nonzero) == []:
                    pass
                else:
                    for i in list(nonzero):
                        tem_list1.append(self.dataset_weight1_table.iloc[each, i])
                    change = np.argsort(tem_list1)
                    new_tem_list1 = []
                    for each_1 in change:
                        new_tem_list1.append(tem_list1[each_1])
                    k = 1
                    change1 = list(np.argsort(new_tem_list1))
                    new_change1 = np.zeros(len(new_tem_list1))
                    for j in change1:
                        new_change1[j] = k
                        k += 1
                    new_final_change = new_change1
                    num = float(np.sum(new_final_change))
                    final_change = new_final_change / float(num)
                    for j in range(0, len(tem_list1)):
                        self.dataset_weight_table.iloc[each, list(nonzero)[j]] = final_change[j]

        for i in range(0, len(self.data_return.index)):
            if np.all(self.data_return.iloc[i, :] == 0.0):
                self.stock_data_return.iloc[i, :] = 0.0
            num_ = float(np.count_nonzero(self.stock_data_return.iloc[i, :]))
            if num_ != 0.0:
                self.stock_data_return.iloc[i, :] = self.stock_data_return.iloc[i, :] / num_ * (0.5)
        self.data_return = self.data_return * -0.5 * self.dataset_weight_table

        self.data_return['market'] = np.sum(self.stock_data_return, axis=1)
        self.data_sum['mode_0'] = np.sum(self.data_return, axis=1)
        print("IR=", self.data_sum.mean(axis=0) / self.data_sum.std(axis=0))
        print('total_return', np.sum(self.data_sum))

        np.cumsum(self.data_sum).plot()
        plt.show()

    def volatility_effect(self):
        volatility_set=[]
        for each_day in self.dataset.keys():
            for each_stock in self.dataset[each_day].keys():
                start_date=datetime.datetime.strptime(each_day,'%Y%m%d')
                while datetime.datetime.strftime(start_date, '%Y%m%d') not in self.stock_data_return.index:
                    start_date += BDay(1)
                start_date = datetime.datetime.strftime(start_date, '%Y%m%d')
                start_day = list(self.stock_data_return.index).index(str(start_date))
                if each_stock in self.stock_data_return.columns and  float(np.std(self.stock_data_return[each_stock][start_day-int(self.test_window):start_day]))>0.0:
                    volatility_set.append(float(np.std(self.stock_data_return[each_stock][start_day+1:start_day+int(test_window)+1]))/\
                            float(np.std(self.stock_data_return[each_stock][start_day-int(self.test_window):start_day])))
        judge_volatility_effect=np.mean(volatility_set)
        print 'volatility_effect is: ',judge_volatility_effect

    def volume_effect(self):
        volume_set=[]
        for each_day in self.dataset.keys():
            for each_stock in self.dataset[each_day].keys():
                start_date = datetime.datetime.strptime(each_day, '%Y%m%d')
                while datetime.datetime.strftime(start_date, '%Y%m%d') not in self.stock_data_return.index:
                    start_date += BDay(1)
                start_date = datetime.datetime.strftime(start_date, '%Y%m%d')
                start_day = list(self.stock_data_return.index).index(str(start_date))
                if each_stock in self.market_volume.columns and float(np.mean(self.market_volume[each_stock][start_day-int(self.test_window):start_day]))>0.0:
                    volume_set.append(float(np.mean(self.market_volume[each_stock][start_day+1:start_day+int(test_window)+1]))/\
                                      float(np.mean(self.market_volume[each_stock][start_day-int(self.test_window):start_day])))
        judge_volume_effect=np.mean(volume_set)
        print 'volume_effect is',judge_volume_effect

    def run(self):
        self.get_signal()
        self.return_mode0()
        #self.volatility_effect()
        #self.volume_effect()



if __name__ == '__main__':
    raw_path=r'E:\\data\\guidance\\'
    holding_day=60
    test_window=30
    result=calculation(raw_path,holding_day,test_window)
    result.run()







