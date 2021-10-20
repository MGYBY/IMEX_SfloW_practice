#!/usr/bin/env python
"""
% This function 

"""
import numpy as np
from mpl_toolkits.mplot3d import Axes3D                      
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm
import matplotlib.tri as mtri

import time
import sys

nx_cells = 400
n_rk = 3
reconst_var = 'phy'

# problem-specific parameters
normal_depth = 0.0031989
normal_velocity = 0.168895

# Define the boundaries x_left and x_right of the spatial domain
x_min = 0.0
x_max = 4.0

y_min = -1.0
y_max = 1.0

obs_width = 0.50
# set a sufficiently large value for the block
obs_height = 1.0
# lower left corner of the obstacle
obs_x1 = 2.0
obs_y1 = (-0.50)*obs_width


# Define the number n_points of points of the grid
nx_points  = nx_cells+1

# Define the grid stepsize dx
dx = ( x_max - x_min ) / ( nx_cells )

# print('dx',dx,x_max - x_min, nx_cells)

# Define the array x of the grid points
x = np.linspace(x_min,x_max,nx_points)

x_cent = np.linspace(x_min+0.5*dx,x_max-0.5*dx,nx_cells)



dy = dx

# print('dy',dy)
# ny_half_cells = int(np.ceil(y_max/dy))
ny_half_cells = int(np.floor(y_max/dy))
print('ny_half_cells')
print(ny_half_cells)
ny_cells = 2*ny_half_cells
ny_points = ny_cells+1

y_min = -dy*ny_half_cells
y_max = -y_min

print('Number of cells in the y-direction')
print(ny_cells)

n_cells = nx_cells * ny_cells

# print(y_min)
# print(y_max) 

# Define the array x of the grid points
y = np.linspace(y_min,y_max,ny_points)

y_cent = np.linspace(y_min+0.5*dy,y_max-0.5*dy,ny_cells)

X, Y = np.meshgrid(x, y)
X_cent, Y_cent = np.meshgrid(x_cent, y_cent)

# print X.shape
# print X_cent.shape

Z = np.zeros_like(X)

Z_cent = np.zeros_like(X_cent)
W_cent = np.zeros_like(X_cent)
H_cent = np.zeros_like(X_cent)
U_cent = np.zeros_like(X_cent)
V_cent = np.zeros_like(X_cent)


# define the topography
for i in range(nx_points-1,-1,-1):
    for j in range(ny_points-1,-1,-1):
        if ((X[j,i]>obs_x1) and (X[j,i]<(obs_x1+obs_width)) and (Y[j,i]>obs_y1) and (Y[j,i]<(obs_y1+obs_width))):
            Z[j,i]=obs_height
            # Z[j,i]=0.0
        else:
            Z[j,i]=0.0
    

# define the initial solution
for i in range(nx_cells):

    for j in range(ny_cells):

        Z_cent[j,i] = 0.25 * ( Z[j,i] + Z[j+1,i] + Z[j,i+1] + Z[j+1,i+1] )  
        # if (Z_cent[j,i]>obs_height/2.0):
        # if (X_cent[j,i]>1.0):
        #     W_cent[j,i] = Z_cent[j,i]
        #     H_cent[j,i] = 0.1
        # else:
        #     W_cent[j,i] = np.float64(normal_depth) + Z_cent[j,i]
        #     # H_cent[j,i] = np.float64(normal_depth)
        #     H_cent[j,i] = 0.0
        # for simplicity, start from dry bed
        # dry-bed leads to zero dt
        H_cent[j,i] = 0.0
        W_cent[j,i] = 0.0 + Z_cent[j,i]
        U_cent[j,i] = 0.0
        V_cent[j,i] = 0.0


# create topography file
header = "ncols     %s\n" % nx_points
header += "nrows    %s\n" % ny_points
header += "xllcorner " + str(x_min-0.5*dx) +"\n"
header += "yllcorner " + str(y_min-0.5*dx) +"\n"
# header += "yllcorner " + str(y_min) +"\n"
# header += "yllcorner " + str(-1.005) +"\n"
header += "cellsize " + str(dx) +"\n"
header += "NODATA_value -9999\n"

print("y_min=")
print(y_min)

output_full = 'topography_dem.asc'

np.savetxt(output_full, Z, header=header, fmt='%1.12f',comments='')


# create initial thickness file
header = "ncols     %s\n" % nx_cells
header += "nrows    %s\n" % ny_cells
header += "xllcorner " + str(np.amin(x_cent-0.5*dx)) +"\n"
header += "yllcorner " + str(np.amin(y_cent-0.5*dx)) +"\n"
header += "cellsize " + str(dx) +"\n"
header += "NODATA_value -9999\n"

output_full = 'pile.asc'

np.savetxt(output_full, H_cent, header=header, fmt='%1.12f',comments='')

# Read in the file
with open('IMEX_SfloW2D.template', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('runname', 'rw')
filedata = filedata.replace('restartfile', 'pile.asc')
filedata = filedata.replace('x_min', str(x_min))
filedata = filedata.replace('y_min', str(y_min))
filedata = filedata.replace('nx_cells', str(nx_cells))
filedata = filedata.replace('ny_cells', str(ny_cells))
filedata = filedata.replace('dx', str(dx))

if reconst_var=='cons':

    print('Linear reconstruction of conservative variables (h+B,hu,hv)')
    filedata = filedata.replace('bc2', 'HU')
    filedata = filedata.replace('bc3', 'HV')
    filedata = filedata.replace('recvar', 'cons')

else:

    print('Linear reconstruction of physical variables (h+B,u,v)')
    filedata = filedata.replace('bc2', 'U')
    filedata = filedata.replace('bc3', 'V')
    filedata = filedata.replace('recvar', 'phys')

filedata = filedata.replace('order', str(n_rk))


# Write the file out again
with open('IMEX_SfloW2D.inp', 'w') as file:
  file.write(filedata)

