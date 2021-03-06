#!/usr/bin/env python
"""
% This function 

"""
import numpy as np                      
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import sys

# if len(sys.argv)==4: 

#     print('Number of cells')
#     a = sys.argv[1]

#     if a.isdigit():

#         n_cells = int(a)
#         print n_cells
 
#     else:
 
#         sys.exit()

# else:

#     print('Please provide three arguments:\n')
#     print('1) Number of cells\n')
#     print('2) Variables to reconstruct: phys or cons\n')
#     print('3) Steps of the RK scheme\n')
#     sys.exit()

normalDepth = 0.0031989
normalVelocity = 0.168895
distPeriod = 0.933
distAmp = 0.05

n_cells = 4000
n_rk = 3
reconst_var = 'phy'


# Define the boundaries x_left and x_right of the spatial domain
x_left = 0.0
x_right = 10.0

y_bottom = 0.0

# Define the number n_points of points of the grid
n_points  = n_cells+1

# Define the grid stepsize dx
dx = ( x_right - x_left ) / ( n_points - 1 )


# Define the array x of the grid points
x = np.linspace(x_left,x_right,n_points)

x_cent = np.linspace(x_left+0.5*dx,x_right-0.5*dx,n_cells)

B = np.zeros((n_points,1))

B_cent = np.zeros_like(x_cent)
w_cent = np.zeros_like(x_cent)
u_cent = np.zeros_like(x_cent)



# define the topography
for i in range(n_points):
    B[i] = 0.0

# define the initial solution
for i in range(n_cells):
    B_cent[i] = 0.5*(B[i]+B[i+1])
    w_cent[i] = normalDepth+B_cent[i]
    u_cent[i] = normalVelocity


# create topography file
header = "ncols     %s\n" % n_points
header += "nrows    %s\n" % 1
header += "xllcorner " + str(x_left-0.5*dx) +"\n"
header += "yllcorner " + str(0-0.5*dx) +"\n"
header += "cellsize " + str(dx) +"\n"
header += "NODATA_value -9999\n"

output_full = 'topography_dem.asc'

np.savetxt(output_full, np.transpose(B), header=header, fmt='%1.12f',comments='')

# create intial solution file
q0 = np.zeros((5,n_cells))

q0[0,:] = x_cent
q0[1,:] = 0.0
q0[2,:] = w_cent
q0[3,:] = (w_cent-B_cent)*u_cent
q0[4,:] = 0.0

np.savetxt('rw_0000.q_2d', np.transpose(q0), fmt='%19.12e') 

with open('rw_0000.q_2d','a') as file:
    file.write('\n')

# Read in the file
with open('IMEX_SfloW2D.template', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('runname', 'rw')
filedata = filedata.replace('restartfile', 'rw_0000.q_2d')
filedata = filedata.replace('x_left', str(x_left))
filedata = filedata.replace('y_bottom', str(y_bottom))
filedata = filedata.replace('n_cells', str(n_cells))
filedata = filedata.replace('dx', str(dx))

if reconst_var=='cons':

    print('Linear reconstruction of conservative variables (h+B,hu,hv)')
    filedata = filedata.replace('bc2', 'HU')
    filedata = filedata.replace('recvar', 'cons')

else:

    print('Linear reconstruction of physical variables (h+B,u,v)')
    filedata = filedata.replace('bc2', 'U')
    filedata = filedata.replace('recvar', 'phys')

filedata = filedata.replace('order', str(n_rk))

# Write the file out again
with open('IMEX_SfloW2D.inp', 'w') as file:
  file.write(filedata)

# create a figure for the plot
fig, ax = plt.subplots()
plt.xlim([0.0,10.0])
plt.ylim([0.0,0.004])

# plot the initial solution and call "line" the plot
line1, = ax.plot(x,B)
line2, = ax.plot(x_cent,w_cent)


plt.show()
