#!bin/env/python

import copy
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import pylab
import fidoProbability as hist


heaterWarmUp = 15

class Greenhouse:

    #def __init__(self, initialTempOutside, initialSun,
    #             diffusion=random.random()/200+0.05,
    #             radiation=random.random()*0+0.25, 
    #             fan=random.random()/100+0.00, 
    #             heater=random.random()*5+5):
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
        if self.state[0]==True: energy+=0#31
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

import urllib2
lastTemp = initial[0]
energy = 0
##thermostat model
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
    
    year =year
    month =month
    hour = i[-4:-2]
    minute =i[len(i)-2:len(i)]
    day = i[-7:-5]
    OutsideTemp = str(monthOfData[i][0])
    Sunlight = str(monthOfData[i][1])
    InsideTemp = str(newTemp)
    CumulativeEnergyUse = str(energy)
    timestamp =i
"""
    payload = '{"year":"' + year + '","month":"' + month + '","day" : "' + day +'","hour":"' + hour + '","OutsideTemp" : "' + OutsideTemp + '","Sunlight" : "'+ Sunlight +  '","InsideTemp" : "' + InsideTemp + '","CumulativeEnergyUse" : "' + CumulativeEnergyUse +'"}'

    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request('http://127.0.0.1:80/flounder/' + timestamp, data=payload)
    request.add_header('Content-Type', 'application/json')
    request.get_method = lambda: 'PUT'
    url = opener.open(request)"""

##intelligent? model
house2 = copy.deepcopy(house1)
Itemps2=[]
energy2=[]
samples = 0
array = None
y=[]
vars = ['dif','fan','rad','heat']

difArr = []
fanArr = []
radArr = []
heatArr = []
energy=0
flag = 0
when = 0

for i in iterator:
    #be simple thermostat at first
    when+=1

    if lastTemp>90: house2.state[0]=True
    elif lastTemp<80: house2.state[0]=False
        
    if lastTemp<65: house2.state[1]=True
    if lastTemp>70: house2.state[1]=False

    if hist.historicalProbs[i[-4:]]>0.05:
        when=0
        flag=1
        
    if when>30: flag = 0
    if flag==1: house2.state[1]=False
    

    newOutput = house2.step(monthOfData[i][0],monthOfData[i][1]/(2*avgCloud))
    newTemp = newOutput[0]
    energy += newOutput[1]
    Itemps2+=[newTemp]
    energy2+=[energy]

    ##build up array for regression
    difArr+=[lastTemp-monthOfData[i][0]]
    if house2.state[0]==False: fanArr+=[0]
    else: fanArr+=[lastTemp-monthOfData[i][0]]
    radArr+=[-monthOfData[i][1]/(2*avgCloud)]
    heatArr+=[-house2.heaterSteps/float(heaterWarmUp)]
    y+=[lastTemp-newTemp]
    lastTemp= newTemp

A = np.array([difArr,fanArr,radArr,heatArr])
print np.linalg.lstsq(A.T,y)[0]
print [house2.dif,house2.fan,house2.rad,house2.heat]

"""
fout = open(year+"_"+month+".csv", "w")
fout.write("Time,OutsideTemp,Sunlight,InsideTemp,CumulativeEnergyUse\n")

for i in iterator:
    fout.write(i+","+str(monthOfData[i][0])+","+
               str(monthOfData[i][1])+","+
               str(monthOfData[i][2])+","+
               str(monthOfData[i][3])+"\n")

"""

###GRAPHING STUFF###

endRange = len(iterator)/30*7
beginRange = len(iterator)/30*0
x=range(0,endRange)
Otemps = [monthOfData[i][0] for i in iterator[beginRange:beginRange+endRange]]
Osun =  [monthOfData[i][1] for i in iterator[beginRange:beginRange+endRange]]
Itemps1 =  [monthOfData[i][2] for i in iterator[beginRange:beginRange+endRange]]
Itemps2 = Itemps2[beginRange:beginRange+endRange]
energy1 =  [monthOfData[i][3] for i in iterator[beginRange:beginRange+endRange]]
energy2 = energy2[:beginRange+endRange]


plt.figure(1)                # the first figure
plt.subplot(211)             # the first subplot in the first figure
plt.plot(x,Otemps)
plt.subplot(211) 
plt.plot(x,Itemps1)         # the second subplot in the first figure
plt.subplot(211)
plt.plot(x,Itemps2)

print len(energy1)
print len(energy2)

plt.figure(2)              # a second figure
plt.subplot(111)
plt.plot(x,energy1)           # creates a subplot(111) by default
plt.plot(x,energy2)

#plt.figure(1)                # figure 1 current; subplot(212) still current
#plt.subplot(211)
#plt.subplot(x,energy2)            # make subplot(211) in figure1 current
#plt.title('Fido AI')   # subplot 211 title

#plt.plot(x,Otemps)
#plt.plot(x,Itemps1)
#plt.plot(x,Itemps2)

#plt.plot(x,energy1)
#plt.plot(x,energy2)

pylab.show()
