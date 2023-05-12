import numpy as np
from Concept_6.IterationLoop import m_tot
# Constant
g = 9.80665
print (m_tot)

# Initial values
V = 15             #m/s
rho = 1.225         #kg/m^3
mu = 1.789*10**-5   #Pa x s

#DATCOM method
cl_alpha = 0.09
cl0 = 0.6
cd0 = 0.02
cd_10 = 0.11        #Cd at alpha of 10 degrees
b = 2.5
S = .7
c = S/b
Re = rho * c * V / mu
AR = b**2/S
cl_10 = cl0 + 10 * cl_alpha
e = (cl_10**2)/(cd_10 - cd0)/(pi * AR)

### GLIDE PHASE ###
#cL_opt = 
#cd_opt = 

### CLIMB PHASE ###



