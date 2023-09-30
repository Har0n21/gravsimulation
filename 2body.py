#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example of 2-body problem simulation with one heavy object in the middle of coordinates system and smaller one orbiting around it.
Gif visualisation will be saved in current directory

Usage: just run the script
"""
import VVCalculation
import render
import numpy as np

#create galaxy-object

gal = VVCalculation.Galaxy()

#define initial states of the objects/stars
mass = 50000
mass2 = 7000
e = 0
l = 10

x1 = l
y1 = 0
z1 = 0
x2 = -mass*l/mass2
y2 = 0
z2 = 0

a = (x1-x2)*(1+e)/(1-e**2)

vel = mass2/(mass+mass2)*np.sqrt((0.1*(mass+mass2))*(2/(x1-x2) - 1/a))
vel2 = mass/(mass+mass2)*np.sqrt((0.1*(mass+mass2))*(2/(x1-x2) - 1/a))
vx = 0
vy = vel
vz = 0

gal.newstar(VVCalculation.star(x1,y1,z1,vx,vy,vz,mass))

vx2 = 0
vy2 = -vel2
vz = 0
gal.newstar(VVCalculation.star(x2,y2,z1,vx2,vy2,vz,mass2)) 

# start calculation 
iterations = 3000
VVCalculation.calculate(gal, 0.1, iterations)    # calculate (galaxt, dt, steps)
#render results
render.rendersim(300, iterations, gal, Trace = True, Autoscale = False, ShowAxes = True)

