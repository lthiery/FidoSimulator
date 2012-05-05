#!bin/env/python

import random
import math
import numpy as np
import matplotlib.pyplot as plt
import pylab

heaterWarmUp = 15

class Greenhouse:

    def __init__(self, initialTempOutside, initialSun,
                 diffusion=random.random()/4+0.25,
                 radiation=random.random()/16+0.25, 
                 fan=random.random()/4+0.25, 
                 heater=random.random()*5+5):
        self.tempI = initialTempOutside + radiation*initialSun
        self.dif=diffusion
        self.fan=fan
        self.heat=heater
        self.heaterSteps = 0
        self.rad=radiation
        
        

    def step(self, tempOutside, sun, wantFan, wantHeater):
        flux=self.dif
        if(wantFan==True): flux += self.fan #if fan is fun flux increases
        
        self.tempI = self.tempI*(1-flux) + tempOutside*flux + self.rad*sun
        
        #if heater is on
        if wantHeater:
            self.heaterSteps+=1 #it heats up
        else: 
            if self.heaterSteps>0: self.heaterSteps-=1

        self.tempI+=self.heat/heaterWarmUp*min(self.heaterSteps,heaterWarmUp)

        return self.tempI


year = '2000'
month = '01'

file1 = open('./64060KBOS'+year+month+'.dat', 'r')
file2 = open('./64050KBOS'+year+month+'.dat', 'r')

def orderedIter(year,month):
    daysInMonth={'01':30, '02':28, '03':31, '04':30, '05':31, '06':30, '07':31,'08':31, '09':30, '10':31, '11':30, '12':31}
    if int(year)%4.0==0.0: daysInMonth['02']='29'
    days = []
    for i in range(1,daysInMonth[month]):
        if i<10: days+=['0'+str(i)]
        else: days+=[str(i)]
    hours = []
    for i in range(0,24):
        if i<10: hours+=['0'+str(i)]
        else: hours+=[str(i)]
    minutes = []
    for i in range(0,60):
        if i<10: minutes+=['0'+str(i)]
        else: minutes+=[str(i)]
    iter = []
    for i in days:
        for j in hours:
            for k in minutes:
                iter+=[year +"_"+month+"_"+i+"_"+j+k]
    return iter

def addToDict(dict, key, value, index):
        temp = dict[key]
        temp[index]=value
        dict[key]=temp

def checkDict(dict,iterator,index):
    prevKey = None
    for i,key in enumerate(iterator):
        if dict[key][index]==None: dict[key][index]=dict[iterator[i-1]][index]
            
monthOfData = {}
iterator = orderedIter(year,month)

thing = 0

for i in iterator:
    monthOfData[i]=[None,None,None]
    
#add all temps from first file
for i in file1:
    line= i.split()
    key = line[1][3:7]+"_"+line[1][7:9]+"_"+line[1][9:11]+"_"+line[1][11:15]
    try: addToDict(monthOfData,key,float(line[7]),0)
    except: pass

checkDict(monthOfData,iterator,0) #clean up data, make sure there's entries everywhere

#add all cloudy measures from second file
for i in file2:
    line= i.split()
    key = line[1][3:7]+"_"+line[1][7:9]+"_"+line[1][9:11]+"_"+line[1][11:15]
    try: addToDict(monthOfData,key,(float(line[2])+float(line[4]))/26.0,1)
    except: pass

checkDict(monthOfData,iterator,1)

initial = monthOfData[iterator[0]]
house = Greenhouse(initial[0],initial[1])
lastTemp = initial[0]

for i in iterator:
    fan = False; heater = False
    if lastTemp>90: fan=True
    if lastTemp<65: heater=True
    newTemp = house.step(monthOfData[i][0],monthOfData[i][1],fan,heater)
    addToDict(monthOfData,i,newTemp,2)
    lastTemp=newTemp

endRange = len(iterator)#/30*3
beginRange = 0#len(iterator)/30*2
x=range(0,endRange)
Otemps = [monthOfData[i][0] for i in iterator[beginRange:beginRange+endRange]]
Osun =  [monthOfData[i][1] for i in iterator[beginRange:beginRange+endRange]]
Itemps =  [monthOfData[i][2] for i in iterator[beginRange:beginRange+endRange]]
plt.plot(x,Otemps)
#plt.plot(x,Osun)
plt.plot(x,Itemps)
pylab.show()

"""
plt.plot(x,temps[:1000])
plt.plot(x,suns[:1000])
plt.plot(x,y1[:1000])
pylab.show()"""
