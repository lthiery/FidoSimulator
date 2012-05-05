#!bin/env/python

import random
import math
import numpy as np
import matplotlib.pyplot as plt
import pylab

class Greenhouse:

    def __init__(self, initialTempOutside, initialSun,
                 diffusion=random.random()/4+0.25,
                 radiation=random.random()/16+0.25, 
                 fan=random.random()/4+0.25, 
                 heater=random.random()*10):
        self.tempI = initialTempOutside + radiation*initialSun
        self.dif=diffusion
        self.fan=fan
        self.heat=heater
        self.rad=radiation
        
        

    def step(self, tempOutside, sun, wantFan, wantHeater):
        flux=self.dif
        if(wantFan==True): flux += self.fan
        
        self.tempI = self.tempI*(1-flux) + tempOutside*flux + self.rad*sun
        
        if(wantHeater): self.tempI+=self.heat

        return self.tempI
year = '2000'
month = '01'

file1 = open('./64060KBOS'+year+month+'.dat', 'r')
file2 = open('./64050KBOS200001.dat', 'r')

monthOfData ={}
#initialize dictionary
daysInMonth={'01':30, '02':28, '03':31, '04':30, '05':31, '06':30, '07':31,
             '08':31, '09':30, '10':31, '11':30, '12':31}
if int(year)%4.0==0.0: daysInMonth['02']=29

for i in range(0,daysInMonth[month]):
    for j in range(0,60):
        for k in range(0,24):
            monthOfData[year +"_"+month+"_"+str(i)+"_"+str(j)+str(k)]=[None,None,None]
        
fails = 0

def addToDict(dict, key, value, index):
        temp = dict[key]
        temp[index]=value
        dict[key]=temp
   
for i in file1:
    line= i.split()
    year = line[1][3:7]
    month = line[1][7:9]
    day = line[1][9:11]
    hour = line[1][11:13]
    min = line[1][13:15]
    key = year +"_"+month+"_"+day+"_"+hour+min
    monthOfData[key]=[None,None,None]
    
    try: addToDict(monthOfData,key,float(line[7]),0)
    except: pass

def checkDict(dict,index):
    prevKey = None
    for i in range(0,daysInMonth[month]):
        for j in range(0,60):
            for k in range(0,24):
                key = year +"_"+month+"_"+str(i)+"_"+str(j)+str(k)
                if dict[key][index]==None:
                    dict[key][index]=dict[prevKey][index]
                prevKey = key
"""
for i in file2:
    line= i.split()
    key = line[1][3:7]+"_"+line[1][7:9]+"_"+line[1][9:11]+"_"+line[1][11:15]
    
    
    try: monthOfData[key]=[monthOfData[key][0],(float(line[2])+float(line[4]))/26.0,None]
    except: 
        monthOfData[key]=[monthOfData[key][0],monthOfData[prevKey][1],None]"""
#    print key, value



"""
for i,j in enumerate(file1):
    try: temps += [float(j.split()[7])]
    except: temps+=[temps[i-1]]

for i,j in enumerate(file2):
    try: suns += [(float(j.split()[2])+float(j.split()[4]))/26]
    except: suns+=[suns[i-1]]

print len(temps)
print len(suns)

house = Greenhouse(temps[0],suns[0])
y1 = [temps[0]]

        fan = False; heater = False;
        if y1[i]>90: fan=True
        if y1[i]<65: heater=True
        y1 += [house.step(v,w,fan,heater)]

x = range(0,len(y1))

print len(y1)

plt.plot(x,temps[:1000])
plt.plot(x,suns[:1000])
plt.plot(x,y1[:1000])
pylab.show()"""
