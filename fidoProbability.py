#!bin/env/python
import copy
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import pylab
import urllib2
import os.path

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

month = '05'

masterDict = {}

for num in range(0,6):
    year = '200'+str(num)
    filename1 = './64060KBOS'+year+month+'.dat'

    if os.path.isfile(filename1): 
        file1 = open('./64060KBOS'+year+month+'.dat', 'r')
        print "file already exists"
    else:
        file1=urllib2.urlopen("ftp://ftp.ncdc.noaa.gov/pub/data/asos-onemin/6406-"+year+"/"+filename1)
        local_file = open(filename1, "w")
        #Write to our local file
        local_file.write(file1.read())
        local_file.close()
        file1= open('./64060KBOS'+year+month+'.dat', 'r')
        print "downloaded fresh copy"
            
    monthOfData = {}
    iterator = orderedIter(year,month)

    for i in iterator:
        monthOfData[i]=[None,None]
    
#add all temps from first file
    for i in file1:
        line= i.split()
        key = line[1][3:7]+"_"+line[1][7:9]+"_"+line[1][9:11]+"_"+line[1][11:15]
        try:  
            addToDict(monthOfData,key,float(line[-1]),0)
        except: pass

    checkDict(monthOfData,iterator,0) #clean up data, make sure there's entries everywhere

    for index,v in enumerate(iterator[:-60]):
        #monthOfData[v][1]=monthOfData[v][0]-monthOfData[iterator[index+15]][0]
        try: masterDict[v[-4:]]+=[monthOfData[v][0]-monthOfData[iterator[index+15]][0]]
        except: masterDict[v[-4:]]=[monthOfData[v][0]-monthOfData[iterator[index+15]][0]]
           
                        
            
            
       
    """
    endRange = len(iterator)/30*29
    beginRange = len(iterator)/30*0
    x=range(0,endRange)
    
    Dtemps = [monthOfData[i][1] for i in iterator[beginRange:beginRange+endRange]]

    plt.plot(x,Dtemps)"""

arbitraryValue = 2
historicalProbs = {}
def logic(x):
    if x>arbitraryValue: return 1 
    else: return 0

def minutesIterator():
    ret = []
    for j in range(0,24):
        for i in range(0,60):
            time = ""
            if j<10: time='0'+str(j)
            else: time=str(j)
            if i<10: time+='0'+str(i)
            else: time+= str(i)
            ret+=[time]  
    return ret

for i in masterDict:
    for j in masterDict[i]:
        try: 
            #print len(masterDict[i])
            #print logic(j)
            historicalProbs[i]+=logic(j)/float(len(masterDict[i]))
        except:
            historicalProbs[i]=logic(j)/float(len(masterDict[i]))

#for i in historicalProbs:
#    print historicalProbs[i]
"""        
y = [historicalProbs[i] for i in minutesIterator()]

x = range(0,len(y))
plt.plot(x,y)        
pylab.show()
"""


