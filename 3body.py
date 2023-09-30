#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example of 3-body problem simulation with one heavy object in the middle of coordinates system and 2 small objects orbiting it
Gif visualisation will be saved in current directory

Usage: just run the script
"""
import VVCalculation
import render
import numpy as np
import math
import matplotlib.pyplot as plt 

#create galaxy object
gal = VVCalculation.Galaxy()

#define initial state of the objects
bhmass2 = 50000
gal.newstar(VVCalculation.star(0, 0, 0, 0, 0, 0, bhmass2))

for i in range(2):
    mass = 5
    xcenter = 0
    ycenter = 0
    r = np.random.uniform(50, 100)
    teta = np.random.uniform(0,2*np.pi)
    x = xcenter + r * np.cos(teta)
    y = ycenter + r * np.sin(teta)
    z = 0
    vel = np.sqrt((mass+bhmass2)*0.1/r)
    
    vv = np.array([y, -x])
    vnorm = vv/np.linalg.norm(vv)
    vx = vnorm[0]*vel 
    if i == 0:    
        vy = vnorm[1]*vel
        vz = 0
    else:
        vy = 0
        vz = vnorm[1]*vel
    gal.newstar(VVCalculation.star(x,y,z,vx,vy,vz,mass)) 


# start calculation 
iterations = 2000
VVCalculation.calculate(gal, 0.1, iterations)    # calculate (galaxt, dt, steps)
# run render
render.rendersim(400, iterations, gal, Trace = True, Autoscale = False, ShowAxes = True)


