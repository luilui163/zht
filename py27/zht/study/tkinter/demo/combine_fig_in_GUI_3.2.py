#-*-coding: utf-8 -*-
#@author:tyhj

def get_fig():
    import matplotlib.pyplot as plt

    # The slices will be ordered and plotted counter-clockwise.
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 10]
    explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig = plt.figure()
    a1 = fig.add_subplot(111)
    a1.pie(sizes, explode=explode, labels=labels,
           autopct='%1.1f%%', shadow=True, startangle=90)
    a1.axis('equal')
    return fig

from tkinter import *
from random import random
from math import sqrt
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
root = Tk()
root.wm_title('Gas')
def pe():
    print(N.get(),Energy.get(),Step.get(),State.get())
def _quit():
    root.quit()
    root.destroy()
def step(atom,Dv):
    for i in range (len(atom)-2):
        dv = -Dv+Dv*2*random()
        if (atom[i]['v']+dv)**2/2-atom[i]['e'] < atom['demon']['e']:
            atom['demon']['e'] += -(atom[i]['v']+dv)**2/2+atom[i]['e']
            atom[i]['v'] = atom[i]['v']+dv
            atom[i]['e'] = (atom[i]['v'])**2/2
    return atom
def ideal_gas(
        N,                              # Number of particles
        totalEnergy,                        # total of demon and system energy
        steps,                          # number of simulation steps
        state,                        # Initial state 1 or 2
    ):
    atom = {}
    for i in range (N):
        atom[i] = {}
        atom[i]['e'] = totalEnergy/N*(2-state)  #depending on state
        atom[i]['v'] = sqrt(atom[i]['e']*2)     # mass=1
    atom['demon'] = {'e':totalEnergy*(state-1)}  #depending on state
    for i in range(steps):
        atom = step(atom,sqrt(2*totalEnergy/N/10))
        atom['demonh'] = atom.get('demonh',[])+[(atom['demon']['e'])]#store energy of demon for figure
    return atom
def gas():
    ideal_gas(N.get(),Energy.get(),Step.get(),State.get())

figure1 = Figure(figsize=(5,4), dpi=100)
figure2 = Figure(figsize=(5,4), dpi=100)
figure3 = Figure(figsize=(5,4), dpi=100)
def draw_picture():
    a1 = figure1.add_subplot(111)
    sys_e = []
    x = []
    total_e = []
    for N in range (50,501,50):
        atom = ideal_gas(N,500,1000,1)
        sys_e.append(500-atom['demon']['e'])
        x.append(N)
        total_e.append(500)
    a1.plot(x,total_e)
    a1.plot(x,sys_e)
    a1.convert_xunits('J')
    a1.set_xlabel("N")
    a1.set_ylabel("Energy")
    a1.set_title('Energy')

    a2 = figure2.add_subplot(111)
    fr = {}
    f = []
    x = []
    for i in range (N):
        fr[atom[i]['v']//1] = fr.get(atom[i]['v']//1,0)+1
    for key in fr:
        x.append(key)
        f.append(fr[key])
    a2.bar(x,f,width = 1)
    a2.convert_xunits('J')
    a2.set_xlabel("v")
    a2.set_ylabel("Frequency")
    a2.set_title('V-Frequency')

    a3 = figure3.add_subplot(111)
    fr = {}
    f = []
    x = []
    for i in range (Step):
        fr[atom['demonh'][i]//1] = fr.get(atom['demonh'][i]//1,0)+1
    for key in fr:
        x.append(key)
        f.append(fr[key])
    a3.bar(x,f,width = 1)
    a3.convert_xunits('J')
    a3.set_xlabel("Demon Energy")
    a3.set_ylabel("Frequency")
    a3.set_title('Demon Energy-Frequency')

def enter():
    gas()
    draw_picture()

def p1():
    fig=get_fig()
    canvas = FigureCanvasTkAgg(fig,root)
    canvas.get_tk_widget().pack(anchor = E , expand=1)
    canvas.show()

def p2():
    canvas = FigureCanvasTkAgg(figure2,root)
    canvas.get_tk_widget().pack(anchor = E ,side=RIGHT, expand=1)
    canvas.show()

def p3():
    canvas = FigureCanvasTkAgg(figure3,root)
    canvas.get_tk_widget().pack(anchor = E ,side=RIGHT, expand=1)
    canvas.show()

canvas = FigureCanvasTkAgg(figure1,root)
canvas.get_tk_widget().pack(anchor = E , expand=1)

root.geometry('960x600')
label_N = Label(root,text = 'Please input the number of atoms:')
label_Energy = Label(root,text = 'Please input the energy of atoms:')
label_Step = Label(root,text = 'Please input the step you want to go:')
N = IntVar()
entry_N = Entry(root,textvariable = N)
entry_N.pack()
Energy = IntVar()
entry_Energy = Entry(root,textvariable = Energy)
entry_Energy.pack()
Step = IntVar()
entry_Step = Entry(root,textvariable = Step)
entry_Step.pack()
button_enter = Button(root,text = 'Enter',command = enter)
button_enter.pack()
button_enter.place(height = 30,width = 100,x = 75,y = 500)
button_quit = Button(root,text = 'Quit',command = _quit)
button_quit.pack()
button_quit.place(height = 30,width = 100,x = 225,y = 500)
label_N.pack()
label_N.place(x = 20,y = 100,anchor = NW)
label_Energy.pack()
label_Energy.place(x = 20,y = 150,anchor = NW)
label_Step.pack()
label_Step.place(x = 20,y = 200,anchor = NW)
entry_N.place(in_=label_N,relx = 1.076)
entry_Energy.place(in_=label_Energy,relx = 1.1)
entry_Step.place(in_=label_Step,relx = 1)
State = IntVar()
radiobutton_demon = Radiobutton(root,variable = State,text = 'Give all the energy to demon',value = 1)
radiobutton_system = Radiobutton(root,variable = State,text = 'Give all the energy to system',value = 2)
radiobutton_demon.pack()
radiobutton_demon.place(x = 20,y = 250)
radiobutton_system.pack()
radiobutton_system.place(x = 20,y = 300)
button_figure1 = Button(root,text = 'Figure1',command = p1)
button_figure2 = Button(root,text = 'Figure2',command = p2)
button_figure3 = Button(root,text = 'Figure3',command = p3)
button_figure1.pack()
button_figure2.pack()
button_figure3.pack()
button_figure1.place(height = 30,width = 100,x = 20,y = 350)
button_figure2.place(height = 30,width = 100,x = 20,y = 400)
button_figure3.place(height = 30,width = 100,x = 20,y = 450)
root.mainloop()









