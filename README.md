# gravsimulation
Simulation and Visualisation of n-body problem (gravitational force only, no collisions ) using Python.


# Overview
This script can calculate and visualise evolution of n-body problem, by calculating gravitational forces between an arbitrary number of bodies and by using Velocity-Verlet numerical method for integration of Newton's equations of motion. The resulting visualisation is saved as .gif file in current directory.

# Usage 
See 3body.py, 2body.py, cluster.py for usage examples and try to play with it.

If you want to start a new calculation from scratch, follow these steps:
1. Create a new .py file in the directory
2. Import core modules: VVCalculation, render
3. Initiate a galaxy with the method of _class galaxy_: VVCalculation.Galaxy()
4. Saturate the galaxy with some stars: gal.newstar( VVCalculation.star( x1,y1,z1,vx,vy,vz,mass ) )
5. Choose number of integration steps needed to be calculated: iterations = 1000
6. Run the calculation by using _calculate_ method from _VVCalculation_ module: VVCalculation.calculate(gal, dt, iterations)
7. Start rendering with the _redersim_ method from _render_ module: render.rendersim(frames, iterations, gal, Trace = True, Autoscale = True, ShowAxes = True)

# Dependencies
[Numba](https://numba.pydata.org/)

# Examples

![3body](https://github.com/Har0n21/gravsimulation/assets/76521092/9f2f406a-de2f-4219-a044-1fbaad70b6f1)

![cluster](https://github.com/Har0n21/gravsimulation/assets/76521092/8f1128e2-3dcb-4181-aa6d-ece634d16078)

![ezgif com-gif-maker](https://github.com/Har0n21/gravsimulation/assets/76521092/b31eaf64-9c86-4914-9098-4df354f85b56)

https://github.com/Har0n21/gravsimulation/assets/76521092/1b57b07d-de95-4b95-a883-9ee27d985fa8
