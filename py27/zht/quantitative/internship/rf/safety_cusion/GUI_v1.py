#-*-coding: utf-8 -*-
#@author:tyhj




'''
把所有数据写成dict形式
value_dict={'long term position':v1,'short term position':v2}


'''
from Tkinter import *


root=Tk()
root.title('安全垫计算器')
root.geometry('500x500')


total_position_ratio=0.2
amount=6000000
cash=6000000
predict_bottom_price=5.12
current_price=8.30
stop_profit_price=9.58
cusion_times=4
short_term_revenue=1935.32
long_term_revenue=1034.34
short_term_ratio=0.8 #default

total_position=amount*total_position_ratio
short_term_position=total_position*short_term_ratio
breakeven_loss_range=1.0/cusion_times
cusion_times_risk_score=2*cusion_times if cusion_times<=5.0 else 10.0
bonus_to_cusion_times_risk_score=((current_price-predict_bottom_price)/(stop_profit_price-predict_bottom_price))*10.0
total_risk_score=cusion_times_risk_score+bonus_to_cusion_times_risk_score
suggested_cusion_times=bonus_to_cusion_times_risk_score
short_term_return=short_term_revenue/short_term_position
def get_long_term_position():
    v=(short_term_revenue+long_term_revenue)*cusion_times
    if v<=total_position*0.2:
        long_term_position=total_position*0.2
    elif v>cash:
        long_term_position=cash
    else:
        long_term_position=v
    return long_term_position

long_term_position=get_long_term_position()
cash_remained=cash-(long_term_position-total_position*0.2)

# def cal(values):
#     total_position_ratio=values['total position ratio']
#     amount=values['amount']
#     cash=values['cash']
#     predict_bottom_price=values['predict bottom price']
#     current_price=values['current price']
#     stop_profit_price=values['stop profit price']
#     cusion_times = values['cusion times']
#     short_term_revenue = values['short term  revenue']
#     long_term_revenue = values['long term revenue']
#     short_term_ratio = values['short term ratio']

class Values:
    def __init__(self,input_values):
        self.total_position_ratio = input_values['total position ratio']
        self.amount = input_values['amount']
        self.cash = input_values['cash']
        self.predict_bottom_price = input_values['predict bottom price']
        self.current_price = input_values['current price']
        self.stop_profit_price = input_values['stop profit price']
        self.cusion_times = input_values['cusion times']
        self.short_term_revenue = input_values['short term revenue']
        self.long_term_revenue = input_values['long term revenue']
        self.short_term_ratio = input_values['short term ratio']

        self.total_position=self.amount*self.total_position_ratio
        self.short_term_position = self.total_position * self.short_term_ratio
        self.breakeven_loss_range = 1.0 / self.cusion_times
        self.cusion_times_risk_score = 2 * self.cusion_times if self.cusion_times <= 5.0 else 10.0
        self.bonus_to_cusion_times_risk_score = ((self.current_price - self.predict_bottom_price) / (
        self.stop_profit_price - self.predict_bottom_price)) * 10.0
        self.total_risk_score = self.cusion_times_risk_score + self.bonus_to_cusion_times_risk_score
        self.suggested_cusion_times = self.bonus_to_cusion_times_risk_score
        self.short_term_return = self.short_term_revenue / self.short_term_position
        self.long_term_position = self.get_long_term_position()
        self.cash_remained = self.cash - (self.long_term_position - self.total_position * 0.2)

    def get_long_term_position(self):
        v = (short_term_revenue + long_term_revenue) * cusion_times
        if v <= total_position * 0.2:
            long_term_position = total_position * 0.2
        elif v > cash:
            long_term_position = cash
        else:
            long_term_position = v
        return long_term_position



def caculate():
    # for k in output_dict:
    #     print k
    #     output_dict[k].insert('insert','123')
    input_values={}
    for k in input_dict:
        input_values[k]=float(input_dict[k].get())
    values=Values(input_values)
    output_dict['total risk score'].insert('insert',values.total_risk_score)
    output_dict['long term position'].insert('insert',values.long_term_position)
    output_dict['breakeven loss range'].insert('insert',values.breakeven_loss_range)
    output_dict['cash remained'].insert('insert',values.cash_remained)
    output_dict['suggested cusion times'].insert('insert',values.suggested_cusion_times)




#input frame
input_frame=Frame(root)
variables_input=['total position ratio','amount','cash','predict bottom price',
           'current price','stop profit price','cusion times','short term revenue',
           'long term revenue','short term ratio']
input_dict={}
for i,v in enumerate(variables_input):
    Label(input_frame,text=v).grid(row=i,sticky=W)
    input_dict[v]=Entry(input_frame)
    input_dict[v].grid(row=i,column=1,sticky=E)
input_frame.pack()








#output frame
'''
查看 study中的132行
'''
output_frame=Frame(root)
variables_output=['total risk score','long term position',
                  'breakeven loss range','cash remained',
                  'suggested cusion times']
output_dict={}
for j,vo in enumerate(variables_output):
    Label(output_frame,text=vo).grid(row=j,sticky=W)
    output_dict[vo]=Entry(output_frame,height=2,textvariable=v,state='readonly')
    output_dict[vo].grid(row=j,column=1,sticky=E)
output_frame.pack(padx=10,pady=10)

Button(root,text='run',bg='blue',width=50,height=3,command=caculate).pack(padx=10,pady=30)

root.mainloop()




'''
clear the entry element,refering to calculator demo
'''









