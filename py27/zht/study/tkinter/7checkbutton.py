#-*-coding: utf-8 -*-
#@author:tyhj
import Tkinter as tk

window=tk.Tk()
window.title('my window')
window.geometry('500x500')

l=tk.Label(window,bg='yellow',width=20,text='empty')
l.pack()

def print_selection():
    if var1.get()==1 and var2.get()==0:
        l.config(text='I love only Python')
    elif var1.get()==0 and var2.get()==1:
        l.config(text='I love only C++')
    elif var1.get()==0 and var2.get()==0:
        l.config(text='I do not have either')
    else:
        l.config(text='I love both')

var1=tk.IntVar()
var2=tk.IntVar()
c1=tk.Checkbutton(window,text='Python',variable=var1,onvalue=1,offvalue=0,command=print_selection)
c2=tk.Checkbutton(window,text='C++',variable=var2,onvalue=1,offvalue=0,command=print_selection)

c2.pack()
c1.pack()

window.mainloop()









