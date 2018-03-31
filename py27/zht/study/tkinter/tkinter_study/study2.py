#-*-coding: utf-8 -*-
#@author:tyhj

from Tkinter import *
root=Tk()

l=Label(root,text='asdglasdj,\n',justify=LEFT,
        padx=10)
l.pack(side=LEFT)
p=PhotoImage(file='a.fig')
abel=Label(root,image=p)
abel.pack(side=RIGHT)

root.mainloop()

#==================
#photo
from Tkinter import *
root=Tk()

photo=PhotoImage(file='bg.fig')
theLabel=Label(root,
               text='学 python\n到FishC',
               justify=LEFT,
               image=photo,
               compound=CENTER,
               font=('华康少女字体',20),
               fg='white')
theLabel.pack()

mainloop()

#=====================================
#button
from Tkinter import *

def callback():
    var.set('吹吧你，我才不信呢~')

root=Tk()

frame1=Frame(root)
frame2=Frame(root)

var=StringVar()
var.set('你所下载的内容含有未成年内容，\n请满18周岁后再点击查看!')
textLabel=Label(frame1,
                textvariable=var,
                justify=LEFT)
textLabel.pack(side=LEFT)

photo=PhotoImage(file='18.gif')
imgLabel=Label(frame1,iamge=photo)
imgLabel.pack(side=RIGHT)

theButton=Button(frame2,text='我已经满18岁',command=callback)
theButton.pack()

frame1.pack()
frame2.pack()

mainloop()

#======================================================
#Checkbutton
from Tkinter import *
root =Tk()

GIRLS=['xisi','diaochang','wangzhaojun','yangyuhuan']
v=[]
for girl in GIRLS:
    v.append(IntVar())
    b=Checkbutton(root,text=girl,variable=v[-1])
    b.pack(anchor=W)

root.mainloop()

#====================================================
#Radiobutton
from Tkinter import *

root=Tk()

group=LabelFrame(root,text='zuihaode jiaobenyuyanshi?',padx=5,pady=5)
group.pack(padx=10,pady=10)

LANGS=[
    ('python',1),
    ('perl',2),
    ('ruby',3),
    ('lua',4)
    ]

v=IntVar()

for lang,num in LANGS:
    b=Radiobutton(group,text=lang,variable=v,value=num)
    b.pack(anchor=W)

mainloop()



#=================================================

from Tkinter import *

root=Tk()

Label(root,text='zuoping:').grid(row=0,column=0)
Label(root,text='zuozhe:').grid(row=1,column=0)

v1=StringVar()
v2=StringVar()


e1=Entry(root,textvariable=v1)
e2=Entry(root,textvariable=v2,show='*')
e1.grid(row=0,column=1,padx=10,pady=5)
e2.grid(row=1,column=1,padx=10,pady=5)

def show():
    print 'zuoping<<%s>>'%e1.get()
    print 'zuoping<<%s>>'%e2.get()

Button(root,text='huoquxinxi',width=10,command=show) \
    .grid(row=3,column=0,sticky=W,padx=10,pady=5)
Button(root,text='huoquxinxi',width=10,command=root.quit) \
    .grid(row=3,column=1,sticky=E,padx=10,pady=5)


mainloop()

#=============================================================
#calculator
from Tkinter import *

master=Tk()

frame=Frame(master)
frame.pack(padx=10,pady=10)

v1=StringVar()
v2=StringVar()
v3=StringVar()

def test(content):
    return content.isdigit()

testCMD=master.register(test)
e1=Entry(frame,width=10,textvariable=v1,validate='key',
         validatecommand=(testCMD,'%P')).grid(row=0,column=0)
Label(frame,text='+')
e2=Entry(frame,width=10,textvariable=v2,validate='key',
         validatecommand=(testCMD,'%P')).grid(row=0,column=1)
Label(frame,text='=').grid(row=0,column=2)
e3=Entry(master,width=10,textvariable=v3,state='readonly').grid(row=0,column=3)

def calc():
    result=int(v1.get())+int(v2.get())
    v3.set(str(result))

Button(frame,text='result',command=calc).grid(row=1,column=2,pady=5)

mainloop()

#===========================================
from Tkinter import *

master=Tk()

theLB=Listbox(master,selectmode=SINGLE)
theLB.pack()


theLB.insert(0,'you are pig')
theLB.insert(END,'you are cat')

theLB.delete(0,END)#delete from 0 to end
theLB.delete(3) #delete the fourth element

for item in ['a','b','c','d']:
    theLB.insert(END,item)

theButton=Button(master,text='delete it',
                 command=lambda x=theLB:x.delete(ACTIVE))
theButton.pack()


mainloop()

#====================================
#scrollbar
from Tkinter import *

root=Tk()

sb=Scrollbar(root)
sb.pack(side=RIGHT,fill=Y)

lb=Listbox(root,yscrollcommand=sb.set)

for i in range(1000):
    lb.insert(END,i)

lb.pack(side=LEFT,fill=BOTH)

sb.config(command=lb.yview)


mainloop()

#==============================================
#scale
from Tkinter import *

root=Tk()

s1=Scale(root,from_=0,to=42,tickinterval=5,resolution=5,length=200)
s1.pack()

s2=Scale(root,from_=0,to=200,tickinterval=50,resolution=10,length=600,orient=HORIZONTAL)
s2.pack()

def show():
    print s1.get(),s2.get()

Button(root,text='get the cursor location',command=show).pack()


mainloop()

#======================================================
#Text
from Tkinter import *

root=Tk()

text=Text(root,width=10,height=2)
text.pack()

text.insert(INSERT,'I love \n')
text.insert(END,'FishC.com')

photo=PhotoImage(file='test.gif')

def show():
    print 'i hoved been clicked'
    text.image_create(END,image=photo)


b1=Button(text,text='click me',command=show)
text.window_create(INSERT,window=b1)

mainloop()

#===========================================
#Canvas

from Tkinter import *

root=Tk()

w=Canvas(root,width=200,height=100)
w.pack()

line1=w.create_line(0,50,200,50,fill='yellow')
line2=w.create_line(100,0,100,100,fill='red',dash=(4,4))
rect1=w.create_rectangle(50,25,150,75,fill='blue')

w.create_text(100,50,text='FishC')
w.create_rectangle(40,20,160,80,dash=(4,4))
w.create_oval(40,20,160,80,fill='pink')




w.coords(line1,0,25,200,25)  #move line1
w.itemconfig(rect1,fill='red')
w.delete(line2)

Button(root,text='delete all the element',command=lambda x=ALL:w.delete(x)).pack()


mainloop()

#==================================================
#event bind
from Tkinter import *

root=Tk()

def callback1(event):
    print 'click location',event.x,event.y

def callback2(event):
    print event.char

def callback3(event):
    print 'current location is:',event.x,event.y

frame=Frame(root,width=200,height=200)

# frame.bind('<Button-1>',callback1)
# frame.pack()

# frame.bind('<Key>',callback2)
# frame.focus_set()
# frame.pack()

frame.bind('<Motion>',callback3)
frame.pack()

mainloop()

#===========================================
from Tkinter import *

root=Tk()

w1=Message(root,text='this is a message',width=100)
w1.pack()

w2=Message(root,text='this a long long long long message',width=200)
w2.pack()

mainloop()

#=======================================
#Spinbox

from Tkinter import *

root=Tk()

# w=Spinbox(root,from_=0,to=10)
w=Spinbox(root,values=['a','b','c','d'])
w.pack()

mainloop()

#===================================

from Tkinter import *


m1=PanedWindow(orient=VERTICAL,showhandle=TRUE)
m1.pack(fill=BOTH,expand=1)

left=Label(m1,text='left pane')
m1.add(left)

m2=PanedWindow(orient=VERTICAL)
m1.add(m2)

top=PanedWindow(orient=VERTICAL)
m2.add(top)

bottom=Label(m2,text='bottom pane')
m2.add(bottom)


mainloop()

#======================================
#Toplevel

from Tkinter import *

root=Tk()

def create():
    top=Toplevel()
    top.attributes('-alpha',0.5)
    top.title('fishC Demo')

    msg=Message(top,text='I love fishc')
    msg.pack()


Button(root,text='create top level window',command=create).pack()

mainloop()

#===========================================
#layout management
#pack grid place

from Tkinter import *

root=Tk()

# photo=PhotoImage(file='logo.gif')
# Label(root,image=photo).grid(row=0,column=2,rowspan=2,padx=5,pady=5)

Label(root,text='user name:').grid(row=0,sticky=W)
Label(root,text='password').grid(row=1,sticky=W)

Entry(root).grid(row=0,column=1)
Entry(root,show='*').grid(row=1,column=1)

Button(text='post',width=10).grid(row=2,columnspan=2,rowspan=3,pady=5)

mainloop()


#=============================
#Dialog
from Tkinter import *

root=Tk()

def callback():
    filename=filedialog.askopenfilename(filetypes=[('PNG','.png'),('GIF','.gif')])
    print filename


Button(root,text='open file',command=callback).pack()

mainloop()
#=========================================================================
#standard dialogs Modules
import tkMessageBox

# tkMessageBox.askokcancel('test','askokcancel')
# tkMessageBox.askquestion('test','question')
# tkMessageBox.askretrycancel('test','askreturycancel')
# tkMessageBox.askyesno('test','askyesno')
tkMessageBox.showerror('test','showerror')
# tkMessageBox.showinfo('test','showinfo')
# tkMessageBox.showwarning("test",'showwarning')
mainloop()

#======================================================
import time
from Tkinter import *
tk=Tk()
canvas=Canvas(tk,width=400,height=200)
canvas.pack()
canvas.create_polygon(10,10,10,60,50,35)
for x in range(0,60):
    canvas.move(1,5,0)
    tk.update()
    time.sleep(0.05)