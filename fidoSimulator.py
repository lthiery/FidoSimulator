#!bin/env/python

import random

class Greenhouse:

    def __init__(self, initialTempOutside, initialSun,
                 diffusion=random.random()/4+0.25,
                 radiation=random.random()/16+0.05, 
                 fan=random.random()/4, 
                 heater=random.random()/4):
        self.tempI = initialTempOutside + radiation*initialSun
        self.dif=diffusion
        self.fan=fan
        self.heat=heater
        self.rad=radiation
        
        

    def step(self, tempOutside, sun, wantFan, wantHeater):
        flux=self.dif
        if(wantFan==True): flux += self.fan
        
        self.tempI = self.tempI*(1-flux) + tempOutside*flux + self.rad*sun
        
        if(wantHeater): self.tempI+=heat

        return (tempOutside,self.tempI)

house = Greenhouse(80,50)
for i in range(0,32):
    print house.step(80,50,False,False)

        
