#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the main render function. It renders using matplotlib.animation module based on calculated data of evolution of coordinates of stars in galaxy-object. Animation is saved as .mp4 file in current
directory.

Usage: rendersim(frames, iterations, gal, Trace = False, Autoscale = False, ShowAxes = True, Dark = False). Parameters: frames - total number of frames required in animation, integer number;
iterations - total number of integration steps (see VVCalculation.calculate); gal - galaxy-object with calculated evolution; Trace - True/False, True if you want to visualize trace of moving stars;
Autoscale - True/False, True if you want to Auto zoomin/zoomout camera view each frame, in order to keep all stars within the camera borders; Showaxes - True/False. True if you want to 
visualize coordinate's system axes; Dark - True/False, True, if you want dark background.
"""

import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import timeit
from mpl_toolkits.mplot3d import Axes3D

def rendersim(frames, iterations, gal, Trace = False, Autoscale = False, ShowAxes = True, Dark = False):
    """
    Parameters: frames - total number of frames required in animation, integer number;
    iterations - total number of integration steps (see VVCalculation.calculate); gal - galaxy-object with calculated evolution; Trace - True/False, True if you want to visualize trace of moving stars;
    Autoscale - True/False, True if you want to Auto zoomin/zoomout camera view each frame, in order to keep all stars within the camera borders; Showaxes - True/False. True if you want to 
    visualize coordinate's system axes; Dark - True/False, True, if you want dark background.
    """
    global DL
    #change scales
    DL = 45 #15000 8     
    j2 = int(iterations/frames)
    
    '''
    xplot = gal.statetime[0][:,0]
    yplot = gal.statetime[0][:,1]
    zplot = gal.statetime[0][:,2]
    maxindex = np.argmax(gal.allmass)
    xmax1 = np.abs(np.amax(xplot))
    xmin1 = np.abs(np.amin(xplot))
    ymax1 = np.abs(np.amax(yplot))
    ymin1 = np.abs(np.amin(yplot))
    zmax1 = np.abs(np.amax(zplot))
    zmin1 = np.abs(np.amin(zplot))
    '''
    
    def sim(j, Autoscale = Autoscale):
        j *= j2    # 1000/25 = 40  (25 fps) 
        
        xplot = gal.statetime[j][:,0]
        yplot = gal.statetime[j][:,1]
        zplot = gal.statetime[j][:,2]
        
        l1._offsets3d = (xplot, yplot, zplot)
        #l1._offsets3d = (gal.statetime[j][:,0], gal.statetime[j][:,1], gal.statetime[j][:,2])   # update position of points
        
        if Autoscale == True:
            
            ax.set_xlim3d(np.amin(xplot) - DL,np.amax(xplot) + DL)
            ax.set_ylim3d(np.amin(yplot) - DL,np.amax(yplot) + DL)
            ax.set_zlim3d(np.amin(zplot) - DL,np.amax(zplot) + DL)
            
            
            '''
            xcenter = gal.statetime[j][maxindex][0]
            ycenter = gal.statetime[j][maxindex][1]
            zcenter = gal.statetime[j][maxindex][2]
            ax.set_xlim3d( xcenter - xmin1,xcenter + xmax1 )
            ax.set_ylim3d( ycenter - ymin1,ycenter + ymax1 )
            ax.set_zlim3d( zcenter - zmin1,zcenter + zmax1 )
            '''
            
        title.set_text('step={}'.format(j))   # show number of frame
        #ax.view_init(30, 0.1 * j/40)  # move view point
        
        #j = j + 50
        #for i in range(len(tracelist)):
        #   tracelist[i][0].set_data(gal.statetime[j-40:j][:,i])
         
        return l1,
    
    fig = plt.figure(figsize = (7,7))  # fig size
    fig.patch.set_visible(False)  # white space
    
    ax = fig.add_subplot(111,projection='3d',
                         xlim=(-5000, 3000), ylim=(-3000, 5000), zlim=(-3000,6000))
    
    if Dark == True:    
        ax.patch.set_facecolor('black')  #background
        
    title = ax.set_title('3D Test')
    ax.set_box_aspect([1,1,1])
   # ax.view_init(90,0)
    # markersize
    markersize = []
    max_mass = np.amax(gal.allmass)
    
    for i in gal.allmass:
        markersize.append(((i/max_mass)*2.5) * 65 + 20)
    
    l1 = ax.scatter(gal.statetime[0][:,0], gal.statetime[0][:,1], gal.statetime[0][:,2], s = markersize)  # set marker size here! 
    
    
    if ShowAxes == False:   
        ax.set_axis_off() # remove axes
    else:
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
    
    if Autoscale == False:

        xplot = gal.statetime[0][:,0]
        yplot = gal.statetime[0][:,1]
        zplot = gal.statetime[0][:,2]
        
        
        ax.set_xlim3d(np.amin(xplot) - DL,np.amax(xplot) + DL)
        ax.set_ylim3d(np.amin(yplot) - DL,np.amax(yplot) + DL)
        ax.set_zlim3d(np.amin(zplot) - DL,np.amax(zplot) + DL)
        '''
        ax.set_xlim3d(-DL, DL)
        ax.set_ylim3d(-DL, DL)
        ax.set_zlim3d(-DL, DL)
        '''
    # add trace plots
    if Trace == True:
        
        global tracelist
        
        tracelist = []
        
        for i in range(np.shape(gal.allmass)[0]):
            tracelist.append(ax.plot(gal.statetime[:,i][:,0],gal.statetime[:,i][:,1],gal.statetime[:,i][:,2],'-'))
            
        
    #save_count = frames/100
    # now 25 fps. interval = 40
    animation1 = FuncAnimation(fig, func = sim, interval = 40, save_count = frames, blit = False) # blit true on linux
    
    
    # start render 
    
    starttime = timeit.default_timer()
    print('renderstart')
    
    animation1.save('animation.gif', writer='PillowWriter', fps=30)
    #animation1.save('manybodyaxes.mp4', writer = "ffmpeg")
    
    stoptime = timeit.default_timer()
    print('rendertime : ', stoptime - starttime)  

    plt.show()