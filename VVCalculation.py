#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is the core module for all the computations/calculations.

It creates Star-objects with a coordinates, mass and initial velocities. Subsequently it also create Galaxy-object, that contains information about the current state of the galaxy, of all
included stars and also information about its evolutions (State in time). This module contains core functions of the calculations: it calculates acceleration vector of each star at
the given state of galaxy (which are the consequence of gravitation interaction between star with each other ) and by using Velocity-Verlet algorithm, 
it does calculate the following position and velocity vectros of stars. By repeating this iteration, it calculates evolution of the state of whole galaxy.

Usage: 
1. Create Galaxy-object: gal = Galaxy()
2. Fill it with some stars: gal.newstar(star(x,y,z,vx,vy,vz,mass)) || See class star() for parameters
3. Run calculations: calculate(gal, 0.1, iterations) || See function calculate(galaxy, dt, steps) for paramets
4. After calculation done, you can access all necessary information about state of the galaxy and stars using methods of class Galaxy(): For example you can obtains current coordinates of all stars by gal.state
5. You can store necessary information using numpy.save method
"""



import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import timeit
from mpl_toolkits.mplot3d import Axes3D
import numba


class star():
    """
    Creates star-object. Parameters (x,y,z,vx,vy,vz,mass): x,y,z - position coordinates, can be any float number; vx,vy,vz - elements of velocity vector, can be any float number;
    mass - mass of the star, can be any positive float number.
    """
    global starlist    
    starlist = []                  
    def __init__(self,x,y,z,vx,vy,vz,mass):   # create star with given pos, speed and mass
        self.star_coord = np.array([x,y,z])                  
        self.star_vel = np.array([vx,vy,vz]) 
        self.mass = mass

        starlist.append(self)
            
class Galaxy():
    """
    Creates a Galaxy-object. No parameters needed
    """
    def __init__(self):
        self.state = np.array([])     # current step coord
        self.allmass = np.array([])    # all masses
        self.speed = np.array([])   # current step speed
        self.statetime = np.array([])    # each step coord
        self.speedtime = np.array([]) # each step speed
        self.acc = np.array([])
        self.perfomance = []
        
    def newstar(self, st):
        """
        Adds star-object into Galaxy-object. Parameters (star): Star-object from class star()
        """
        self.allmass = np.append(self.allmass, st.mass)
        if len(self.state) == 0:
            self.state = np.array([st.star_coord])
            self.speed = np.array([st.star_vel])
        else:
            self.speed = np.append(self.speed, [st.star_vel], axis = 0)
            self.state = np.append(self.state, [st.star_coord],axis = 0)

@numba.jit(nopython=True)
def acceleration(state, allM, G = 0.1):
    """
    Calculates acceleration applied on each star due to Newton-Gravitational-force. Parameters (state, allM, G=1): state - Galaxy.state method, that contains information about the latest coordinates
    of all stars. allM - Galaxy.allmass method, which contains array of masses of all stars. G - any float number, gravitational coefficient. 
    """
    allacc = np.zeros(np.shape(state))
    
    galaxy2 = np.copy(state)
    allM2 = np.copy(allM)
    allM3 = np.copy(allM2)
    galaxy5 = np.copy(state)

    
    for i in range(np.shape(state)[0] - 1):            # roll matrix, calculate acc
        for j in range(np.shape(galaxy2)[0]):
            galaxy2[j] = galaxy5[j-1]
            allM2[j] = allM3[j-1]
        allM3 = np.copy(allM2)
        galaxy5 = np.copy(galaxy2)    
        

        galaxy3 = np.subtract(galaxy2, state)
        
        # calculate Rij
        modul_r3 = np.power(np.sum(np.power(galaxy3,2), axis = 1),1.5) # calculate |Rij|**3
        
        '''
        for i in range(np.shape(modul_r3)[0]):
            if modul_r3[i] < 0.000001:
                modul_r3[i] = 0.000001
                '''

            
        allacc += allM3.reshape(allM3.shape + (1,))  * (galaxy3/modul_r3.reshape(modul_r3.shape+(1,)))


    return allacc * G 


def initial(galaxy):
    galaxyacc = acceleration(galaxy.state, galaxy.allmass)
    galaxyacc2 = np.empty([np.shape(galaxy.allmass)[0],3])
    for i in range(np.shape(galaxy.allmass)[0]):
        wz = np.sqrt(np.linalg.norm(galaxyacc[i])/np.linalg.norm(galaxy.state[i]))  
        
        galaxyacc2[i]= np.cross(np.array([0,0,wz]),galaxy.state[i])
        
    
    galaxy.speed = galaxyacc2

    
def VVA(galaxy, dt, step):   # add globalglobal coords
    """
    Verlet-velocity algorthim. Parameters (galaxy, dt, step): galaxy - galaxy-object; dt - integration step size, positive number; step - current integration step, integer.
    """
    galaxy.state = galaxy.state + galaxy.speed * dt + 1/2 * (galaxy.acc * (dt**2) ) 
    galaxyacc2 = acceleration(galaxy.state, galaxy.allmass)
    galaxy.speed = galaxy.speed + 1/2 * (galaxy.acc + galaxyacc2) * dt
    galaxy.acc = galaxyacc2
    galaxyevolv[step + 1] = galaxy.state
    galaxyevsp[step + 1] = galaxy.speed

def calculate(galaxy, dt, steps):   # run VV algorithmus. set dt and umber of frames/steps
    """
    Main calculation functions. Parameters (galaxy,dt,steps): galaxy - galaxy-object, dt - integration step size, positive number; step - total number of steps needed to be integrated
    """
    global stepsglobal
    stepsglobal = steps
    
    starttime = timeit.default_timer()

    print('Calculationstart')
    
    global galaxyevolv, galaxyevsp
    
    galaxyevolv = np.empty([steps + 1, np.shape(galaxy.allmass)[0],3])
    galaxyevsp = np.empty([steps + 1, np.shape(galaxy.allmass)[0],3])
    galaxy.acc = acceleration(galaxy.state, galaxy.allmass)
    
    galaxyevolv[0] = galaxy.state
    galaxyevsp[0] = galaxy.speed
    
    for i in range(steps):  # number of steps
        
        VVA(galaxy, dt, i)
        
        
        if i%10 == 0:
                print(i)
                pasttime = timeit.default_timer()
                print('Timepassed : ', pasttime - starttime) 
                

    
    stoptime = timeit.default_timer()
    print('CalculationTime : ', stoptime - starttime) 
    galaxy.statetime = galaxyevolv
    galaxy.speedtime = galaxyevsp