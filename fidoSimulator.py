#!bin/env/python

import copy
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import pylab

heaterWarmUp = 15

class Greenhouse:

    def __init__(self, initialTempOutside, initialSun,
                 diffusion=random.random()/100,
                 radiation=random.random()/8+0.25, 
                 fan=random.random()/100+0.005, 
                 heater=random.random()*5+5):
        self.tempI = initialTempOutside + radiation*initialSun
        self.dif=diffusion
        self.fan=fan
        self.heat=heater
        self.heaterSteps = 0
        self.rad=radiation
        self.state=[False,False]

    def step(self, tempOutside, sun):
        
        flux=self.dif
        if(self.state[0]==True): flux += self.fan #if fan is fun flux increases
        
        self.tempI = self.tempI*(1-flux) + tempOutside*flux + self.rad*sun
        #self.tempI = self.tempI - (tempOutside-self.tempI)**2*flux + self.rad*sun
        #if heater is on
        if self.state[1]==True:
            self.heaterSteps+=1 #it heats up
        else: 
            if self.heaterSteps>0: self.heaterSteps-=1

        self.tempI+=self.heat/heaterWarmUp*min(self.heaterSteps,heaterWarmUp)

        energy = 0 ##calculate hypothetical energy usage
        if self.state[0]==True: energy+=31
        if self.state[1]==True: energy+=175

        return (self.tempI,energy)

###BRINGING THE DATA IN AND CLEANING IT UP###
year = '2000'
month = '05'

file1 = open('./64060KBOS'+year+month+'.dat', 'r')
file2 = open('./64050KBOS'+year+month+'.dat', 'r')

def orderedIter(year,month):
    daysInMonth={'01':30, '02':28, '03':31, '04':30, '05':31, '06':30, '07':31,'08':31, '09':30, '10':31, '11':30, '12':31}
    if int(year)%4.0==0.0: daysInMonth['02']=29
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

for i in iterator:
    monthOfData[i]=[None,None,None,None]
    
#add all temps from first file
for i in file1:
    line= i.split()
    key = line[1][3:7]+"_"+line[1][7:9]+"_"+line[1][9:11]+"_"+line[1][11:15]
    try: addToDict(monthOfData,key,float(line[7]),0)
    except: pass

checkDict(monthOfData,iterator,0) #clean up data, make sure there's entries everywhere

#add all cloudy measures from second file
hiCloud = None
loCloud = None
sum=0
samples=0 

for i in file2:
    line= i.split()
    key = line[1][3:7]+"_"+line[1][7:9]+"_"+line[1][9:11]+"_"+line[1][11:15]
    try: 
        cloudValue = (float(line[2])+float(line[4]))
        sum+=cloudValue; samples+=1
        if cloudValue<=1:
            addToDict(monthOfData,key,cloudValue,1)
        if hiCloud ==None: 
            hiCloud = cloudValue
            loCloud = hiCloud
        else:
            hiCloud = max(cloudValue,hiCloud)
            loCloud = min(cloudValue,loCloud)        
    except: pass

avgCloud = sum/float(samples)
print avgCloud
checkDict(monthOfData,iterator,1)

###SIMULATING###
initial = None
house1 = None
i=0
while True:
    try: 
        initial = monthOfData[iterator[i]]
        house1 = Greenhouse(initial[0],initial[1])
        break
    except:
        i+=1

lastTemp = initial[0]
energy = 0
for i in iterator:

    if lastTemp>90: house1.state[0]=True
    elif lastTemp<80: house1.state[0]=False

    if lastTemp<65: house1.state[1]=True
    if lastTemp>70: house1.state[1]=False
    newOutput = house1.step(monthOfData[i][0],monthOfData[i][1]/(2*avgCloud))
    newTemp = newOutput[0]
    energy += newOutput[1]
    addToDict(monthOfData,i,newTemp,2)
    addToDict(monthOfData,i,energy,3)
    lastTemp=newTemp

fout = open(year+"_"+month+".csv", "w")
fout.write("Time,OutsideTemp,Sunlight,InsideTemp,CumulativeEnergyUse\n")

for i in iterator:
    fout.write(i+","+str(monthOfData[i][0])+","+
               str(monthOfData[i][1])+","+
               str(monthOfData[i][2])+","+
               str(monthOfData[i][3])+"\n")

house2 = copy.deepcopy(house1)

###GRAPHING STUFF###

endRange = len(iterator)/30*7
beginRange = len(iterator)/30*0
x=range(0,endRange)
Otemps = [monthOfData[i][0] for i in iterator[beginRange:beginRange+endRange]]
Osun =  [monthOfData[i][1] for i in iterator[beginRange:beginRange+endRange]]
Itemps =  [monthOfData[i][2] for i in iterator[beginRange:beginRange+endRange]]
energy =  [monthOfData[i][3] for i in iterator[beginRange:beginRange+endRange]]
plt.plot(x,Otemps)
plt.plot(x,Itemps)
pylab.show()

print house.heater


