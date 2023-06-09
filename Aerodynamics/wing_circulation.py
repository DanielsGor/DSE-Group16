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
c_r, alpha_root, b_s = 0.2, 6, 0.9


#Iteration calculations
n_discretisations = 1000 #m

def calculate_lift_distribution (alpha_root_local, c_r_local, b_s_local):

    #main lifting wing
    L_total_req = m*g
    L_plasma = cl_p * rho * V**2 * S_p2 #1/2 is taken out since its factored out in the twist rate calculation
    twist_rate = (c_r_local * (alpha_root_local-alpha_cl0) * b_w2 + (alpha_root_local-alpha_cl0)*(c_p-c_r_local)/(b_w2-b_s_local) * (b_w2**2 -b_s_local**2)/2 - (L_total_req-L_plasma)/ (rho * V**2 * cl_alpha_w))/(c_r_local*b_w2**2/2 + (c_p-c_r_local)/(b_w2-b_s) * (b_w2**3 -b_s_local**3)/3)
    
    n_w = n_discretisations * np.ceil(b_w2/b2 * 100)/100
    dyi_w = b_w2/n_w #added n_discretisations
    dyi_s = b_s_local/n_w #added n_discretisations

    cs = []
    angles = []
    lifts = []
    ys = []
    diffs = []
    ideals = []
    cls = []
    
    for yi in np.linspace(0,b_s_local, int(np.ceil(b_s_local/b2 * n_discretisations))):    
        c_yi =  c_r_local
        S_yi = c_yi * dyi_s

        alpha_yi = alpha_root_local - yi*twist_rate
        if np.abs (alpha_yi) > 15:
            alpha_yi = 0
        
        correctional_factor_for_lift = -6.566*yi**6 + 27.609*yi**5 -44.472*yi**4 + 34.027*yi**3 - 12.528*yi**2 + 1.9309*yi -0.0835  #numbers from xflr5 comparing 2d to 3d case of straight wing
        cl_yi = (alpha_yi - alpha_cl0)*cl_alpha_w * (1+correctional_factor_for_lift)

        local_param = cl_yi* 1/2 *rho * V**2 * c_yi
        local_ideal = gamma0 * rho * V* np.sqrt(1-(2*yi/b_total)**2)
        
        cls.append(S_yi)
        diffs.append((local_param-local_ideal)**2)
        lifts.append(local_param)
        ys.append(yi)
        ideals.append(local_ideal)
        cs.append(c_yi)
        angles.append(alpha_yi)

    for yi in np.linspace(b_s_local,b_w2, int(np.ceil((b_w2-b_s_local)/b2 * n_discretisations))):    
        c_yi =  (c_p -c_r_local)*((yi-b_s)/(b_w2-b_s)) + c_r_local
        S_yi = c_yi * dyi_w

        alpha_yi = alpha_root_local - yi*twist_rate
        if np.abs (alpha_yi) > 15:
            alpha_yi = 0
        
        correctional_factor_for_lift = -6.566*yi**6 + 27.609*yi**5 -44.472*yi**4 + 34.027*yi**3 - 12.528*yi**2 + 1.9309*yi -0.0835  #numbers from xflr5 comparing 2d to 3d case of straight wing
        cl_yi = (alpha_yi - alpha_cl0)*cl_alpha_w * (1+correctional_factor_for_lift)

        local_param = cl_yi* 1/2 *rho * V**2 * c_yi
        local_ideal = gamma0 * rho * V* np.sqrt(1-(2*yi/b_total)**2)
        
        cls.append(S_yi)
        diffs.append((local_param-local_ideal)**2)
        lifts.append(local_param)
        ys.append(yi)
        ideals.append(local_ideal)
        cs.append(c_yi)
        angles.append(alpha_yi)
    n_p = n_discretisations - n_w 
    dyi_p = b_p2 / n_p #added n_discretisations

    #control wing
    for yi in np.linspace (b_w2,b_w2+b_p2,n_discretisations-int(np.ceil(b_s_local/b2 * n_discretisations))-int(np.ceil((b_w2-b_s_local)/b2 * n_discretisations))):
        cl_yi = cl_p
        c_yi = c_p
        alpha_yi = 8 #deg 
        S_yi = dyi_p * c_yi
        correctional_factor_for_lift = -6.566*yi**6 + 27.609*yi**5 -44.472*yi**4 + 34.027*yi**3 - 12.528*yi**2 + 1.9309*yi -0.0835  #numbers from xflr5 comparing 2d to 3d case of straight wing
        local_param = cl_yi* 1/2 *rho * V**2 * c_yi * (1+correctional_factor_for_lift)
        local_ideal = gamma0 * rho * V* np.sqrt(1-(2*yi/b_total)**2) 
        
        cls.append(S_yi)
        diffs.append((local_param-local_ideal)**2)
        lifts.append(local_param)
        ys.append(yi)
        ideals.append(local_ideal)
        cs.append(c_yi)
        angles.append(alpha_yi)

    total_diff = sum(diffs,0)
    return total_diff, lifts, ideals, cs, angles, cls, ys, twist_rate


print ('completing final results', c_r, alpha_root, b_s)

diffs, lifts, ideals, cs, angles, cls, ys, twist_rate = calculate_lift_distribution(alpha_root_local=alpha_root, c_r_local=c_r,b_s_local = b_s)

plt.plot(ys, lifts, label = 'real')
plt.plot(ys, ideals, label = 'ideal')
plt.legend()
plt.show()

#chord
plt.plot(ys, [-c for c in cs], label = 'chord')
plt.plot(ys, [0] * len(ys))
plt.legend()
plt.show()

#angle
plt.plot(ys, angles, label = 'angle')
plt.legend()
plt.show()


print (c_r, alpha_root, b_s, twist_rate)