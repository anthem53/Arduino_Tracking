# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 17:10:44 2021

@author: gkgk0
"""

import time
import tkinter
import joystickSerial 
from tkinter import *

import random
import math


'''
#system const value or method
'''
# joystick coord to canvas coord
def j2c (x,y):
    return [x,1023-y]

def getMiddlePoint(l):
        return [(l[0] + l[2])/2 , (l[1]+l[3])/2 ]


middle = [519,516]

getDirection = lambda b, t : ([  (b[i] - t[i])   for i in [0,1]])
getMiddleDirection = lambda b : getDirection (b,middle)
getCanvasDirection = lambda b : [b[0],-b[1]]
getDistance = lambda b, t : sum([  (b[i] - t[i]) ** 2  for i in [0,1]])**(1/2)


canvasWidth = 900
canvasHeight =700

''' 
window option setting
'''
window = tkinter.Tk()
window.title("Joystick GUI TEST")
window.geometry("1200x800+2000+50")
window.resizable(False,False)

canvas =tkinter.Canvas(window,width= canvasWidth, height = canvasHeight, relief = 'groove' ,bd=5)
canvas.pack()

''' joyStick  option setting'''
myJoystick = joystickSerial.Joystick()
def quit():
    myJoystick.close()
    window.destroy()
    
    
    
B = Button(window,width=10 ,height= 5,text = "Quit" ,  command = quit)
B.place(x = 10,y = 10)


class Player :
    def __init__(self):
        self.obj = canvas.create_oval(100, 200, 125, 225, fill="blue", width=3)
        self.xAccel = 0
        self.yAccel = 0
        
    def move(self):
        canvas.move(self.obj, self.xAccel, self.yAccel)
    
        
    def updateAccel(self,x,y):
        
        place = canvas.coords(self.obj)
        
        if place[0] + x < 0 :
            self.xAccel = -place[0]
        elif place[2] + x > canvasWidth :
            self.xAccel = canvasWidth - place[2]
        else:
            self.xAccel = x
        
        if place[1] + y < 0 :
            self.yAccel = -place[1]
        elif place[3] + y > canvasHeight :
            self.yAccel = canvasHeight - place[3]
        else:
            self.yAccel= y
    
      
      
    def currentPlace(self):
        return canvas.coords(self.obj)

class Goal :
    def __init__(self):
        self.obj = canvas.create_oval(400,400,425,425 , fill="red", width = 3)
    def setNewPlace(self):
        random.seed()
        
        newX = random.randint(0,canvasWidth-25)
        newY = random.randint(0,canvasHeight-25)
        
        canvas.coords(self.obj,newX,newY, newX+25, newY+25)
        time.sleep(0.25)
    def currentPlace(self):
        return canvas.coords(self.obj)

class Route :
    def __init__(self,player,goal):
        pp = player.currentPlace()
        gp = goal.currentPlace()
        
        pp = self.getMiddlePoint(pp)
        gp = self.getMiddlePoint(gp)
          
        self.start = pp
        self.end = gp
            
        self.obj = canvas.create_line(pp[0],pp[1],gp[0],gp[1])
    def getMiddlePoint(self,l):
        return [(l[0] + l[2])/2 , (l[1]+l[3])/2 ]
 
    def setNewPlace(self,player,goal):
        pp = player.currentPlace()
        gp = goal.currentPlace()
        
        pp = self.getMiddlePoint(pp)
        gp = self.getMiddlePoint(gp)
        
        self.start = pp
        self.end = gp
            
        canvas.coords(self.obj,pp[0],pp[1],gp[0],gp[1])
    def getStart(self):
        return self.start
    def getEnd(self):
        return self.end
        

class Game:
    def __init__(self):
        self.goal = Goal()
        self.player = Player()
        self.route = Route(self.player,self.goal)
        
    def start(self):
        while True:
    
            #newXY = [0,0]
            newXY = getCanvasDirection(getMiddleDirection(myJoystick.getCoord()))
            
            const = 400
            self.player.updateAccel(newXY[0]/const,newXY[1]/const)
            self.player.move()
            isCollision = self.checkCollision()
            
            print("충돌: " + str(isCollision))
            if isCollision == True :
                self.goal.setNewPlace()
                self.route.setNewPlace(self.player, self.goal)
            
            print("점과 직선사이 거리 : " +str(self.getDistancefromRoute()))
            print("점과 점 사이 거리 : " + str(self.getDistancefromGoal()))
            window.update()
            
    def checkCollision(self):
        goalPlace = canvas.coords(self.goal.obj)
        playerPlace = canvas.coords(self.player.obj)
        
        playerPlaceList = []
        for i in [0,2]:
            for j in [1,3]:
                playerPlaceList.append([playerPlace[i],playerPlace[j]])
        
        for x,y in playerPlaceList :
            if (x >= goalPlace[0]  and x <= goalPlace[2]):
                if (y >= goalPlace[1]  and y <= goalPlace[3]):
                    return True
                
        return False
    
    def getDistancefromGoal(self):
        end = self.route.getEnd()
        player = getMiddlePoint(self.player.currentPlace())
        
        return getDistance(player, end) -25
    
    def getDistancefromRoute(self):
        start = self.route.getStart()
        end = self.route.getEnd()
        
        # y = ax + b
        a = (end[1]- start[1]) / (end[0] - start[0])
        b = end[1] - a * end[0]

        # ax - y + b = 0, (x1,y1)        
        
        pp = getMiddlePoint(self.player.currentPlace())
        
        return abs(a*pp[0] - pp[1] + b) /  (a*a + 1)**(1/2)
        
   


game = Game()
game.start()



window.mainloop()