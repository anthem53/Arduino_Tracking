# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 15:11:40 2021

@author: gkgk0
"""

import serial
import time
import tkinter
import joystickSerial 
from tkinter import *


window = tkinter.Tk()
window.title("Joystick GUI TEST")
window.geometry("800x700+2000+100")

window.resizable(False,False)
myJoystick = joystickSerial.Joystick()

def quit():
    myJoystick.close()
    window.destroy()
    
    
B = Button(window,width=10 ,height= 5,text = "Quit" ,  command = quit)
B.place(x = 10,y = 10)

canvas =tkinter.Canvas(window,width= 540, height = 540, relief = 'groove' ,bd=2)
canvas.pack()



player = canvas.create_oval(100, 200, 150, 250, fill="blue", width=3)





while True:
    xy = myJoystick.getCoord() 
    print()
    x = xy[0]
    y = xy[1]
    
    print(xy)
    canvas.coords(player, x/2 + 2, 512- y/2, (x/2 + 2)+25, (512- y/2)+25)
    window.update()



window.mainloop()