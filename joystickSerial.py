# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import serial
import time


ser = None
keymap = ["n",'↙','↓','↘','←','중립','→','↖','↑','↗']

def bytesCorrect(input):
    
    l = list(input)
    l2 = list(reversed(l))
    
    a = [chr(x) for x in l2]
    
    result = []
    
    result.append(l2[0])
    result.append(l2[1])
    
    l2 = l2[2:]
    
    for i in l2:
        if i == 32:
            result.append(i)
        elif i >=48 and i <= 57:
            result. append(i)
        else:
            break
        
    
    result = bytes(list(reversed(result)))
    
    return result


def findDirection (x,y):
    
    low = 150
    high = 850
    
    arrow = 0
    
    if x < low:
        arrow += 1
    elif x > high:
        arrow += 3
    else:
        arrow += 2
        
    if y < low:
        arrow += 0
    elif y > high:
        arrow += 6
    else:
        arrow += 3 
    
    return arrow

     

def TEST():
    
    ser = serial.Serial('COM3',9600)

    count = 0
    epoch = 1000
    
    while True:
        
        if ser.readable():
            inputData = bytesCorrect(ser.readline())
            
            inputData = inputData.decode("utf-8")
            inputData = inputData.split();
            
            
            if len(inputData) <2:
                print("joystick Error")
                #ser.close()
                #ser = serial.Serial('COM3',9600)
                time.sleep(0.05)
                continue
            
            x = int(inputData[0])
            y = int(inputData[1])
            print("x : " + str(x))
            print("y : " + str(y) )
            print("레버 입력 : " + str(keymap[findDirection(x, y)] ) + "\n")
                
        
            
        count = count + 1
        if count > epoch :
            print("테스트 종료")
            break
            
    ser.close()  


''' What you use  '''
class Joystick:
    def __init__(self):
        self.serial = serial.Serial('COM3',9600)
    def __del__(self):
        print("joystick destroy call")
        self.serial.close()
        
    def getCoord(self):
        
        while(True) :
        
            xy = self.serial.readline()
            if (len(xy) < 4 ):
                print("serial readline error")
                continue
            xy = bytesCorrect(xy)
            xy = xy.decode()
            xy = [int(x)%1024 for x in xy.split()]
             
            if len(xy) < 2 :
                print("joystickError")
                continue
            return xy
    
    def close(self):
        self.serial.close()
    


#TEST()