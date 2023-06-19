import numpy as np
import matplotlib.pyplot as plt

### Constants ###
# general
m = 8.44#kg
g = 9.81 #m/s2
rho = 1.225 #kg/m3
V = 15 #m/s
b_total = 3 #m
b2 = b_total/2 #m for semi wing

# airfoil parameters
# plasma wing 
cl_alpha_p = 0.1 #1/deg
S_p2 = 0.01697/2 #m
c_p = 0.1692 #m 
b_p2 = S_p2/c_p #
cl_alpha_p = 0.08333 #fixed from fixed angle from plasma performance
gamma0 = m*g / (V*b_total * rho * np.pi/4)

#lifting wing
alpha_tip  = 0
cl_alpha_w = 0.108 #1/deg
b_w2 = b2  -b_p2#m for semi wing
alpha_cl0 = -6

#horizontal tail sizing
b_htail = 1.52
b_htail2 = b_htail/2 

#vertical tail sizing
b_vtail = 0.54
b_vtail2 = b_vtail/2

#Iteration calculations
n_discretisations = 1000 #m

#correctional factor
A,B,C,D,E,F,G = -8.0359,33.427,-52.59,38.899,-13.763,1.8618,0.9312

#Input parametesr
alpha_tip  = 0
b_s = 0.9 #m
c_r  = 0.2 #m

roll_rate_max = np.deg2rad(11.92) #deg/s #positive along x axis 

def calculate_restoring_moment (c_r_local, b_s_local):

    #twist_rate = (L_total_req /(rho * V **2 * cl_alpha_w) +(alpha_cl0 - alpha_tip)*(c_r_local*P_n_y(1,b_w2) + (c_p-c_r_local)/b_w2 * (P_n_y(2,b_w2)- P_n_y(2,b_s_local))))/(c_r_local*b_w2*P_n_y(1,b_w2) - c_r_local * P_n_y(2,b_w2)+ (c_p -c_r_local) * (P_n_y(2,b_w2)-P_n_y(2,b_s_local)) -(c_p-c_r_local)/b_w2 * (P_n_y(3,b_w2)-P_n_y(3,b_s_local)))
    n_w = n_discretisations * np.ceil(b_w2/b2 * 100)/100
    dyi_w = b_w2/n_w #added n_discretisations

    cs = []
    angles = []
    ys = []
    cls = []
    M = 0
    
    #main wing straight section
    for yi in np.linspace(0,b_s_local, int(np.ceil(b_s_local/b2 * n_discretisations))):    
        c_yi =  c_r_local

        alpha_induced = - np.arctan (roll_rate_max*yi / V)
        
        correctional_factor_for_lift = A*yi**6 + B *yi**5 + C*yi**4 + D *yi**3 + E*yi**2 + F*yi +G  #numbers from xflr5 comparing 2d to 3d case of straight wing
        delta_cl_yi = alpha_induced*cl_alpha_w * (correctional_factor_for_lift)

        M += yi * delta_cl_yi* 1/2 *rho * V**2 * c_yi
    
        cls.append(delta_cl_yi)
        ys.append(yi)
        cs.append(c_yi)
        angles.append(alpha_induced)

    #main wing tapered section
    for yi in np.linspace(b_s_local,b_w2, int(np.ceil((b_w2-b_s_local)/b2 * n_discretisations))):    
        c_yi =  (c_p -c_r_local)*((yi-b_s_local)/(b_w2-b_s_local)) + c_r_local
        S_yi = c_yi * dyi_w

        alpha_induced = - np.arctan (roll_rate_max*yi / V)
        
        correctional_factor_for_lift = A*yi**6 + B *yi**5 + C*yi**4 + D *yi**3 + E*yi**2 + F*yi +G  #numbers from xflr5 comparing 2d to 3d case of straight wing
        delta_cl_yi = alpha_induced*cl_alpha_w * (correctional_factor_for_lift)

        M += yi * delta_cl_yi* 1/2 *rho * V**2 * c_yi
        
        cls.append(delta_cl_yi)
        ys.append(yi)
        cs.append(c_yi)
        angles.append(alpha_induced)

    n_p = n_discretisations - n_w 
    dyi_p = b_p2 / n_p #added n_discretisations
    c_yi = c_p

    #control wing
    for yi in np.linspace (b_w2,b_w2+b_p2,n_discretisations-int(np.ceil(b_s_local/b2 * n_discretisations))-int(np.ceil((b_w2-b_s_local)/b2 * n_discretisations))):
        alpha_induced = - np.arctan (roll_rate_max*yi / V)
        
        correctional_factor_for_lift = A*yi**6 + B *yi**5 + C*yi**4 + D *yi**3 + E*yi**2 + F*yi +G  #numbers from xflr5 comparing 2d to 3d case of straight wing
        delta_cl_yi = alpha_induced*cl_alpha_p * (correctional_factor_for_lift)

        M += yi * delta_cl_yi* 1/2 *rho * V**2 * c_yi
    
        cls.append(delta_cl_yi)
        ys.append(yi)
        cs.append(c_yi)
        angles.append(alpha_induced)

    #htail
    for yi in np.linspace (0,b_htail2, int(np.ceil(n_discretisations * b_htail2/b2))):
        alpha_induced = - np.arctan (roll_rate_max*yi / V)
        
        delta_cl_yi = alpha_induced*cl_alpha_p

        M += yi * delta_cl_yi* 1/2 *rho * V**2 * c_yi
    
        cls.append(delta_cl_yi)
        ys.append(yi)
        cs.append(c_yi)
        angles.append(alpha_induced)

    #vtail
    for yi in np.linspace (0,b_vtail2, int(np.ceil(n_discretisations * b_vtail2/b2))):
        alpha_induced = - np.arctan (roll_rate_max*yi / V)
        
        delta_cl_yi = alpha_induced*cl_alpha_p

        M += yi * delta_cl_yi* 1/2 *rho * V**2 * c_yi
    
        cls.append(delta_cl_yi)
        ys.append(yi)
        cs.append(c_yi)
        angles.append(alpha_induced)

    return cs, angles, cls, ys, 2*M

cs, angles, cls, ys, total_restoring_moment = calculate_restoring_moment(c_r_local=c_r, b_s_local=b_s)

print (total_restoring_moment)

plt.plot (ys, angles)
plt.show()

plt.plot (ys, cls)
plt.show()