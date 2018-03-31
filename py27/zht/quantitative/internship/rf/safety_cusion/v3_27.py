#-*-coding: utf-8 -*-
#@author:tyhj

import Tkinter
import tkMessageBox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root=Tkinter.Tk()
root.title('safety cusion calculator')
root.geometry('800x600')

#==================================================================================
#default values and calculator logic
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

default_input_values={'total position ratio':total_position_ratio,
                      'amount':amount,
                      'cash':cash,
                      'predict bottom price':predict_bottom_price,
                      'current price':current_price,
                      'stop profit price':stop_profit_price,
                      'cusion times':cusion_times,
                      'short term revenue':short_term_revenue,
                      'long term revenue':long_term_revenue,
                      'short term ratio':short_term_ratio
                      }

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
#=================================================================================================


input_dict={}
output_dict={}
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


def initial_input_values():
    for k in input_dict:
        input_dict[k].delete(0,Tkinter.END)
        input_dict[k].insert(Tkinter.END,default_input_values[k])

def verify_input_values():
    for k in input_dict:
        content=input_dict[k].get()
        try:
            float(content)
        except ValueError:
            tkMessageBox.showerror('data input error','the value format is invalid in %s'%k)
            return False
    return True

def calculate():
    flag=verify_input_values()
    if flag:
        input_values={}
        for k in input_dict:
            if input_dict[k].get()=='':
                print ('test')
                input_dict[k].insert(Tkinter.END, default_input_values[k])
                input_values[k]=default_input_values[k]
            else:
                input_values[k]=float(input_dict[k].get())

        values=Values(input_values)
        clear_output_result()
        output_dict['total risk score'].insert(Tkinter.END,values.total_risk_score)
        output_dict['long term position'].insert(Tkinter.END,values.long_term_position)
        output_dict['breakeven loss range'].insert(Tkinter.END,values.breakeven_loss_range)
        output_dict['cash remained'].insert(Tkinter.END,values.cash_remained)
        output_dict['suggested cusion times'].insert(Tkinter.END,values.suggested_cusion_times)


def clear_output_result():
    for k in output_dict:
        output_dict[k].delete(0,Tkinter.END)

def clear_input_entry():
    for k in input_dict:
        input_dict[k].delete(0,Tkinter.END)

def get_fig():

    import matplotlib.pyplot as plt

    # The slices will be ordered and plotted counter-clockwise.
    labels = 'cusion_times_risk_score','bonus_to_cusion_times_risk_score'
    sizes = [60,40]
    explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')
    fig=plt.figure(figsize=(5, 4), dpi=50)
    a1=fig.add_subplot(111)
    a1.pie(sizes, explode=explode, labels=labels,
            autopct='%1.1f%%', shadow=True, startangle=90)
    a1.axis('equal')
    return fig

def config():
    #=======================================================================================
    #input frame
    input_frame=Tkinter.LabelFrame(root)
    variables_input=['total position ratio','amount','cash','predict bottom price',
               'current price','stop profit price','cusion times','short term revenue',
               'long term revenue','short term ratio']
    for i,v in enumerate(variables_input):
        Tkinter.Label(input_frame,text=v).grid(row=i,sticky=Tkinter.W)
        input_dict[v]=Tkinter.Entry(input_frame)
        input_dict[v].grid(row=i,column=1,sticky=Tkinter.E)
    input_frame.grid(row=0,column=0,padx=10,pady=5,sticky=Tkinter.W)
    # =================================================================================================
    # fig frame
    fig_frame = Tkinter.LabelFrame(root)
    fig = get_fig()
    canvas = FigureCanvasTkAgg(fig, fig_frame)
    canvas.get_tk_widget().pack(anchor=Tkinter.E, expand=1)
    canvas.show()
    # Label(fig_frame,image=fig_pie)
    fig_frame.grid(row=1,column=0,sticky=Tkinter.W,padx=10,pady=5)
    #===============================================================================================
    #output frame
    output_frame=Tkinter.LabelFrame(root)
    variables_output=['total risk score','long term position',
                      'breakeven loss range','cash remained',
                      'suggested cusion times']
    for j,vo in enumerate(variables_output):
        Tkinter.Label(output_frame,text=vo).grid(row=j,sticky=Tkinter.W)
        output_dict[vo]=Tkinter.Entry(output_frame)
        output_dict[vo].grid(row=j,column=1,sticky=Tkinter.E)
    # Button(output_frame,text='detail',bg='green',command=fig_pie).grid(row=0,column=2,sticky=E)
    # output_frame.pack(padx=10,pady=10)
    output_frame.grid(row=0,column=1,sticky=Tkinter.W)
    # Button(root,text='calculate',bg='blue',width=50,height=3,command=calculate).pack(padx=10,pady=30)
    Tkinter.Button(root, text='calculate', bg='blue', width=50, height=3, command=calculate) \
        .grid(row=2,column=0,sticky=Tkinter.W,padx=10,pady=5)

def run():
    config()
    initial_input_values()
    root.mainloop()



if __name__=='__main__':
    run()


'''
clear the entry element,refering to calculator demo
'''














