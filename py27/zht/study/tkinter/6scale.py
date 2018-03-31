#-*-coding: utf-8 -*-
#@author:tyhj

import Tkinter as tk

window=tk.Tk()
window.title('my window')
window.geometry('500x500')

'''
label 的width 和height的单位是字符
scale中的单位是pixel
'''
l=tk.Label(window,bg='yellow',width=20,text='empty')
l.pack()

def print_selection(v):
    l.config(text='you have selected'+v)

s=tk.Scale(window,label='try me',from_=5,to=11,
           orient=tk.HORIZONTAL,length=200,
           showvalue=0,tickinterval=3,resolution=0.01,
           command=print_selection

           )
#resolution 是为了确定保留小数位数
#showvalue 标示是否显示数值
s.pack()


window.mainloop()
