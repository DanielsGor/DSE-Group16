import numpy as np
#from Concept_6.IterationLoop import m_tot
# Constant
g = 9.80665
m_tot = 6.459211578395105
W_tot = m_tot * g

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
e = (cl_10**2)/(cd_10 - cd0)/(np.pi * AR)
cl_max = 1.6
ROC = 2.8

V_stall = np.sqrt(m_tot*g/S*2/rho*1/cl_max)

### GLIDE PHASE ###
cl_g = np.sqrt (cd0*np.pi*AR*e)
cd_g = cd0 + cl_g**2 /(np.pi*AR*e)

gamma_g = np.arctan(cd_g/cl_g)
V_g = np.sqrt(W_tot/S*2/rho*1/cl_g)
assert V_g > V_stall, 'Velocity too low'

x_g = V_g * np.cos(gamma_g)

### CLIMB PHASE ###
cl_c = np.sqrt (3*cd0*np.pi*AR*e)
cd_c = cd0 + cl_c**2 /(np.pi*AR*e)

polynomial = np.poly1d([cl_c**2 * 0.25 * rho**2 * S**2,0,0,0,-W_tot**2,0,ROC**2*W_tot**2])
V_c = np.real(polynomial.r[0])
gamma_c = np.arcsin(ROC/V_c)

T_c = cd_c * 0.5 * rho * V_c**2 * S + W_tot*np.sin(gamma_c)
assert T_c < 15.582494498240683, 'Not enough thrust available' #max thrust available from propulsion
y_c = 80

x_c = y_c/np.tan(gamma_c)

print (x_g/x_c)



