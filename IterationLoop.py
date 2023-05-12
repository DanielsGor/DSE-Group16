import numpy as np 


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
#print ('c:', c)
Re = rho * c * V / mu
#print('Re:', Re) 
AR = b**2/S
#print (AR)
cl_10 = cl0 + 10 * cl_alpha
e = (cl_10**2)/(cd_10 - cd0)/(np.pi * AR)
#print('e:', e)
eff = 0.8
eff_prop = 0.8
eff_motor = 0.9
endurance = 2 #h 
energy_density = 170 # Wh/kg

### TAKE OFF calculations (for thrust) ###
def TO_thrust(W):
    climb_angle = np.arcsin(ROC_requirement/V)
    cL_TO = W* np.cos(climb_angle) / (0.5*rho*V**2 * S)
    #angle_TO = (cL_TO - cl0)/cl_alpha
    cd_TO = cd0 + cL_TO**2 /(np.pi*AR*e)
    T_TO  = W*np.sin(climb_angle) + cd_TO*0.5*rho*V**2*S
    return T_TO

def C_thrust (W):
    cL_cruise = np.sqrt(3*cd0*np.pi*AR*e)
    #L_cruise = cL_cruise*0.5*rho*V**2*S
    #angle_cruise = (cL_cruise-cl0)/cl_alpha
    cd_cruise = cd0 + cL_cruise**2/(np.pi*AR*e)
    T_cruise = cd_cruise*0.5*rho*V**2 * S
    return T_cruise

def Power_calc(T, eff_prop, eff_motor):
    P = T*V/(eff_motor*eff_prop)
    return P

def prop_M_TO (W, eff_prop = eff, eff_motor= eff):
    T = TO_thrust(W)
    P = Power_calc(T, eff_prop = eff, eff_motor= eff)
    if P<10 or P>600:
        print ('EXTRAPOLATED PROPULSION MASS BASED ON PROPULSION:', P)
    
    m1, p1 = 2.7, 10
    m2, p2= 70, 200
    dmdp = (m2-m1)/(p2-p1)
    M = m1 + (P-p1) * dmdp
    
    return M/1000

def bat_M_C(W,Endurance,eff_prop, eff_motor):
    T = C_thrust(W)
    P = Power_calc( T, eff_prop, eff_motor)
    E = P * Endurance #Wh
    M_bat = E/energy_density
    return M_bat

dW = 100
while dW > 0.01:
    print (W_tot)
    m_bat = bat_M_C(W_tot, endurance, eff_prop, eff_motor)
    m_prop = prop_M_TO(W_tot, eff_prop, eff_motor)
    W_temp = ((0.43 + 0.09 +0.1)*5.55 + 1 + m_bat + m_prop ) * g
    dW = W_tot - W_temp
    W_tot = W_temp
    
print ('Weight:',W_temp, '\nmass:', W_temp/g,'\n Propulsion mass:', m_bat, '\n Battery mass:', m_bat)
#print(W_tot)
