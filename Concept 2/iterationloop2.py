import numpy as np

# Using DATCOM
# based on 'Static Stability Analysis on Twin Tail... Angga Septiyana, ...'

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
cl_alpha = (2*np.pi*np.pi)/(180)
cl0 = 0
cd0 = 0.02
b = 2.2
S = .69
c = S/b
Re = rho * c * V / mu
AR = b**2/S
cl_10 = cl0 + 10 * cl_alpha
cd_10 = cl_10/12 #Cd at alpha of 10 degrees
e = (cl_10**2)/(cd_10 - cd0)/(np.pi * AR)
eff = 0.8
eff_prop = 0.8
eff_motor = 0.9
endurance = 2 #h
energy_density = 170 # Wh/kg


### TAKE OFF calculations (for thrust) ###
def TO_thrust(W):
    climb_angle = np.arcsin(ROC_requirement / V)
    cL_TO = W * np.cos(climb_angle) / (0.5 * rho * V ** 2 * S)
    # angle_TO = (cL_TO - cl0)/cl_alpha
    cd_TO = cd0 + cL_TO ** 2 / (np.pi * AR * e)
    T_TO = W * np.sin(climb_angle) + cd_TO * 0.5 * rho * V ** 2 * S
    return T_TO


def C_thrust(W):
    cL_cruise = np.sqrt(3 * cd0 * np.pi * AR * e)
    # L_cruise = cL_cruise*0.5*rho*V**2*S
    # angle_cruise = (cL_cruise-cl0)/cl_alpha
    cd_cruise = cd0 + cL_cruise ** 2 / (np.pi * AR * e)
    T_cruise = cd_cruise * 0.5 * rho * V ** 2 * S
    return T_cruise


def Power_calc(T, eff_prop, eff_motor):
    P = T * V / (eff_motor * eff_prop * 0.9)
    return P


def prop_M_TO(W, eff_prop=eff, eff_motor=eff):
    T = TO_thrust(W)
    P = Power_calc(T, eff_prop=eff, eff_motor=eff)/2
    if P < 10 or P > 600:
        print('EXTRAPOLATED PROPULSION MASS BASED ON PROPULSION:', P)

    m1, p1 = 2.7, 10
    m2, p2 = 70, 200
    dmdp = (m2 - m1) / (p2 - p1)
    M = m1 + (P - p1) * dmdp

    return M / 1000 * 2


def bat_M_C(W, Endurance, eff_prop, eff_motor):
    T = C_thrust(W)
    P = Power_calc(T, eff_prop, eff_motor)
    E = P * Endurance  # Wh
    M_bat = E / energy_density
    return M_bat, E


dW = 100
while dW > 0.01:
    # print(W_tot)
    m_bat, E = bat_M_C(W_tot, endurance, eff_prop, eff_motor)
    m_prop = prop_M_TO(W_tot, eff_prop, eff_motor)
    W_temp = ((0.43 + 0.09 + 0.1) * 5.55 + 1 + m_bat + m_prop) * g
    dW = W_tot - W_temp
    W_tot = W_temp

print('Weight:', W_temp, '\nmass:', W_temp / g, '\n Propulsion mass:', m_prop, '\n Battery mass:', m_bat, '\n Energy req:', E)