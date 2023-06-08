import numpy as np
import matplotlib.pyplot as plt

### Constants ###
# general
m = 7.65 #kg
g = 9.81 #m/s2
rho = 1.225 #kg/m3
V = 15 #m/s
b_total = 2.9 #m
b2 = b_total/2 #m for semi wing


# airfoil parameters
# plasma wing 
cl_alpha_p = 0.1 #1/deg
S_p2 = 0.01697/2 #m
c_p = 0.1692 #m 
b_p2 = S_p2/c_p #
cl_p = 0.8 #fixed from fixed angle from plasma performance
gamma0 = m*g / (V*b_total * rho * np.pi/4)

#lifting wing
cl_alpha_w = 0.108 #1/deg
b_w2 = b2  -b_p2#m for semi wing
alpha_cl0 = -6

#Iteration calculations
n_discretisations = 100 #m
c_r = 0.25
alpha_root = 4

def calculate_lift_distribution (n_discretisations_local, alpha_root_local, c_r_local):

    #main lifting wing
    L_total_req = m*g
    L_plasma = cl_p * rho * V**2 * S_p2 #1/2 is taken out since its factored out in the twist rate calculation
    twist_rate = ((alpha_root_local-alpha_cl0)*c_r_local*b_w2 + (c_p-c_r_local)*b_w2 / 2 * (alpha_root_local-alpha_cl0) - (L_total_req - L_plasma)/(cl_alpha_w * rho * V**2))/(c_r_local * b_w2**2 / 2 + (c_p -c_r_local) * b_w2**2 / 3)
    dyi_w = b_w2/np.ceil(b_w2/b2)
    print (twist_rate)
    cs = []
    angles = []
    lifts = []
    ys = []
    diffs = []
    ideals = []
    print (np.ceil(b_w2/b2 * n_discretisations_local))
    for yi in np.linspace(0,b_w2, int(np.ceil(b_w2/b2 * n_discretisations_local))):    
        c_yi =  (c_p -c_r_local)*(yi/b_w2) + c_r_local
        S_yi = c_yi * dyi_w

        alpha_yi = alpha_root_local - yi*twist_rate

        cl_yi = (alpha_yi - alpha_cl0)*cl_alpha_w

        local_param = cl_yi* +1/2 *rho * V**2 * S_yi
        local_ideal = gamma0 * rho * V* np.sqrt(1-2*yi/b_total)
        
        diffs.append(np.sqrt(local_param**2-local_ideal**2))
        lifts.append(local_param)
        ys.append(yi)
        ideals.append(local_ideal)
        cs.append(c_yi)
        angles.append(alpha_yi)
        # print (twist_rate)
        # print(b_w2)
    return diffs, lifts, ideals, cs, angles,ys



diffs, lifts, ideals, cs, angles, ys = calculate_lift_distribution(n_discretisations_local=n_discretisations, alpha_root_local=alpha_root, c_r_local=c_r)
plt.plot(ys, lifts, label = 'real')
plt.plot(ys, ideals, label = 'ideal')
plt.legend()
plt.show()

#chord
plt.plot(ys, cs, label = 'chord')
plt.legend()
plt.show()

#angle
plt.plot(ys, angles, label = 'angle')
plt.legend()
plt.show()

    # #control wing
    # for yi in np.linspace (b_w,b_w+b_p,)