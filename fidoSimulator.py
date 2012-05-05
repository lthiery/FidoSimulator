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

tempI = 60
sunI = 50
house = Greenhouse(tempI,sunI)
temps = [70]
y1 = [tempI]
suns = [50]
endRange = 1024

for i in range(0,endRange):

    temperature = 70+25*np.sin(i*math.pi/124)
    sun = max(0,50*np.sin(i*math.pi/124))
    fan = False; heater = False;
    if y1[i]>90: fan=True
    if y1[i]<65: heater=True
    suns += [sun]
    temps += [temperature]
    y1 += [house.step(temperature,sun,fan,heater)]

x = range(0,endRange+1)


plt.plot(x,temps)
plt.plot(x,suns)
plt.plot(x,y1)
pylab.show()
