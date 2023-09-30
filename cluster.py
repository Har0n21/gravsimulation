#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example of interaction of two star clusters with total 351 objects.

Usage: just run the script

"""
import VVCalculation
import render
import numpy as np
import math

#create galaxy cluster
gal = VVCalculation.Galaxy()

#add heavy objects in the middle of the clusters
bhmass = 10e10
gal.newstar(VVCalculation.star(0, 0, 0, 0, 0, 0, bhmass))


bhmass2 = 30e7
gal.newstar(VVCalculation.star(25000, 0, 0, 0, 130, 0, bhmass2))

e = 0

#saturate clusters with stars
for i in range(300):
    mass = np.random.uniform(4,24)
    xcenter = 0 
    ycenter = 0
    r = np.random.uniform(2500, 7500)
    teta = np.random.uniform(0,2*np.pi)
    x = xcenter + r * np.cos(teta)
    y = ycenter + r * np.sin(teta)
    a = r*(1+e)/(1-e**2)
    z = 0
    vel = bhmass/(mass+bhmass)*np.sqrt((0.1*(mass+bhmass))*(2/(r) - 1/a))

    vv = np.array([y, -x])
    vnorm = vv/np.linalg.norm(vv)
    vx = vnorm[0]*vel
    vy = vnorm[1]*vel
    vz = 0
    gal.newstar(VVCalculation.star(x,y,z,vx,vy,vz,mass)) 
    
for i in range(50):
    mass = np.random.uniform(4,24)
    xcenter = 25000 
    ycenter = 0
    r = np.random.uniform(2500, 7500)
    teta = np.random.uniform(0,2*np.pi)
    x = xcenter + r * np.cos(teta)
    y = ycenter + r * np.sin(teta)
    a = r*(1+e)/(1-e**2)
    z = 0
    vel = bhmass2/(mass+bhmass2)*np.sqrt((0.1*(mass+bhmass2))*(2/(r) - 1/a))
    vv = np.array([-y, x - 25000])
    vnorm = vv/np.linalg.norm(vv)
    vx = vnorm[0]*vel
    vy = vnorm[1]*vel + 100
    vz = 0
    gal.newstar(VVCalculation.star(x,y,z,vx,vy,vz,mass)) 


# start calculation 

iterations = 1000
VVCalculation.calculate(gal, 0.1, iterations)    # calculate (galaxt, dt, steps)
#start rendering
render.rendersim(400, iterations, gal, Trace = False, Autoscale = False, ShowAxes = True)

