import numpy as np
import pandas as pd
from math import pi


# Constant
g = 9.80665

# Initial values
V = 15             #m/s
rho = 1.225         #kg/m^3
mu = 1.789*10**-5   #Pa x s
m_tot = 6.555       #kg
m_pay = 1           #kg
m_OE = m_tot - m_pay

W_tot = m_tot * g
W_pay = m_pay * g
OEW = m_OE * g
ROC_requirement = 2.8 #m/s

#Using DATCOM
#based on 'Static Stability Analysis on Twin Tail... Angga Septiyana, ...'
cl_alpha = 0.09
cl0 = 0.6
cd0 = 0.02
cd_10 = 0.11        #Cd at alpha of 10 degrees
b = 2.5
S = .7
c = S/b
print ('c:', c)
Re = rho * c * V / mu
print('Re:', Re) 
AR = b**2/S
print (AR)
cl_10 = cl0 + 10 * cl_alpha
e = (cl_10**2)/(cd_10 - cd0)/(pi * AR)
print('e:', e)


### LIFT-DRAG MAX calculations ###

cl_LDmax = np.sqrt(pi*AR*e*cd0)  #lowest drag cruise is at 3-4°
angleLDmax = (cl_LDmax - cl0 ) / cl_alpha

L_LDmax = cl_LDmax * 0.5 * rho * V**2 * S
cdLDmax = cd0 + cl_LDmax **2 / (pi * AR * e)
D_LDmax = cdLDmax * 0.5 * rho * V**2 * S  

### Cruise configuration ###
cL_cruise = np.sqrt(3*cd0*pi*AR*e)
L_cruise = cL_cruise*0.5*rho*V**2*S
angle_cruise = (cL_cruise-cl0)/cl_alpha
cd_cruise = cd0 + cL_cruise**2/(pi*AR*e)
T_cruise = cd_cruise*0.5*rho*V**2 * S

### TAKE OFF calculations (for thrust) ###
climb_angle = np.arcsin(ROC_requirement/V)
cL_TO = W_tot * np.cos(climb_angle) / (0.5*rho*V**2 * S)
angle_TO = (cL_TO - cl0)/cl_alpha
cd_TO = cd0 + cL_TO**2 /(pi*AR*e)

T_TO  = W_tot*np.sin(climb_angle) + cd_TO*0.5*rho*V**2*S

#Ignore this it resulted in a value >1 which doesnt make sense
"""#Now using XFLR5 method from the paper because our e was way too high (0.907382)
#based on 'Static Stability Analysis on Twin Tail... Angga Septiyana, ...'
Cl_alpha = 0.09
Cl0 = 0.6
Cd0 = 0.005
Cd_10 = 0.065        #Cd at alpha of 10 degrees
A = 8.77

Cl_10 = Cl0 + 10 * Cl_alpha
e = (Cl_10**2)/(Cd_10 - Cd0)/(pi * A)
print(e)"""


