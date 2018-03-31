#-*-coding: utf-8 -*-
#@author:tyhj


import Tkinter as tk

window=tk.Tk()
window.title('my window')
window.geometry('500x500')

canvas=tk.Canvas(window,bg='blue',height=300,width=500)
# image_file=tk.PhotoImage(file=r'C:\Users\hp\Desktop\test.jpg')
# image=canvas.create_image(0,0,anchor='nw',image=image_file)
x0,y0,x1,y1=200,200,240,240
line=canvas.create_line(x0,y0,x1,y1)
oval=canvas.create_oval(x0,y0,x1,y1,fill='red')
arc=canvas.create_arc(x0+30,y0+30,x1+30,y1+30,start=0,extent=120)
rect=canvas.create_rectangle(100,30,100+20,30+20)

def moveit():
    canvas.move(rect,0,10)

canvas.pack()
b=tk.Button(window,text='move',command=moveit).pack()

window.mainloop()









