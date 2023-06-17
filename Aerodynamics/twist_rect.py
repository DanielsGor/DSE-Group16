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

#Iteration calculations
n_discretisations = 1000 #m

def P_n_y (N,y):
    A,B,C,D,E,F,G = -6.566, 27.609, -44.472, 34.027, -12.528, 1.9309, 0.9165 #0,0,0,0,0,0,1#
    val = 0
    if N == 0:
        n =6
        val = A*y**6 + B*y**5 + C*y**4 + D*y**3 + E*y**2 + F*y + G
    else:
        n = 6 + N
        val = A/n*y**n + B/(n+1)*y**(n+1) + C/(n+2)*y**(n+2) + D/(n+3)*y**(n+3) + E/(n+4)*y**(n+4) + F/(n+5)*y*(n+5) + G/(n+6)*y**(n+6)
    return val

A,B,C,D,E,F,G = -8.025,33.375,-52.504,38.835,-13.743,1.8572,0.9314
A,B,C,D,E,F,G = -8.0359,33.427,-52.59,38.899,-13.763,1.8618,0.9312

def calculate_lift_distribution (c_r_local, b_s_local, final = False):

    #main lifting wing
    L_total_req = m*g
    L_plasma = cl_alpha_p*alpha_tip * rho * V**2 * S_p2 #1/2 is taken out since its factored out in the twist rate calculation
     
    #twist_rate = (L_total_req /(rho * V **2 * cl_alpha_w) +(alpha_cl0 - alpha_tip)*(c_r_local*P_n_y(1,b_w2) + (c_p-c_r_local)/b_w2 * (P_n_y(2,b_w2)- P_n_y(2,b_s_local))))/(c_r_local*b_w2*P_n_y(1,b_w2) - c_r_local * P_n_y(2,b_w2)+ (c_p -c_r_local) * (P_n_y(2,b_w2)-P_n_y(2,b_s_local)) -(c_p-c_r_local)/b_w2 * (P_n_y(3,b_w2)-P_n_y(3,b_s_local)))
    twist_rate = ((L_total_req-L_plasma)/(rho * V**2 * cl_alpha_w) - c_r_local * (alpha_tip-alpha_cl0)* b_w2  - (alpha_tip - alpha_cl0)*(c_p-c_r_local)/b_w2 * (b_w2**2-b_s_local**2)/2)/(c_r_local*b_w2**2 - c_r_local*b_w2**2/2+ (b_w2 *( c_p -c_r_local))/b_w2 * (b_w2**2-b_s_local**2)/2  - (c_p - c_r_local)/b_w2 * (b_w2**3 - b_s_local**3)/3)
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

        alpha_yi = alpha_tip + twist_rate*b_w2 - yi*twist_rate
        if np.abs (alpha_yi) > 15:
            alpha_yi = 0
        
        correctional_factor_for_lift = A*yi**6 + B *yi**5 + C*yi**4 + D *yi**3 + E*yi**2 + F*yi +G  #numbers from xflr5 comparing 2d to 3d case of straight wing
        cl_yi = (alpha_yi - alpha_cl0)*cl_alpha_w * (correctional_factor_for_lift)

        local_param = cl_yi* 1/2 *rho * V**2 * c_yi
        local_ideal = gamma0 * rho * V* np.sqrt(1-(2*yi/b_total)**2)
        if not final:
            diffs.append((local_param-local_ideal)**2)
        else:
            cls.append(S_yi)
            lifts.append(local_param)
            ys.append(yi)
            ideals.append(local_ideal)
            cs.append(c_yi)
            angles.append(alpha_yi)

    for yi in np.linspace(b_s_local,b_w2, int(np.ceil((b_w2-b_s_local)/b2 * n_discretisations))):    
        c_yi =  (c_p -c_r_local)*((yi-b_s)/(b_w2-b_s)) + c_r_local
        S_yi = c_yi * dyi_w

        alpha_yi = alpha_tip + twist_rate*b_w2 - yi*twist_rate

        if np.abs (alpha_yi) > 15:
            alpha_yi = 0
        
        correctional_factor_for_lift = A*yi**6 + B *yi**5 + C*yi**4 + D *yi**3 + E*yi**2 + F*yi +G  #numbers from xflr5 comparing 2d to 3d case of straight wing
        cl_yi = (alpha_yi - alpha_cl0)*cl_alpha_w * (correctional_factor_for_lift)

        local_param = cl_yi* 1/2 *rho * V**2 * c_yi
        local_ideal = gamma0 * rho * V* np.sqrt(1-(2*yi/b_total)**2)
        
        if not final:
            diffs.append((local_param-local_ideal)**2)
        else:
            cls.append(S_yi)
            lifts.append(local_param)
            ys.append(yi)
            ideals.append(local_ideal)
            cs.append(c_yi)
            angles.append(alpha_yi)
    n_p = n_discretisations - n_w 
    dyi_p = b_p2 / n_p #added n_discretisations

    #control wing
    for yi in np.linspace (b_w2,b_w2+b_p2,n_discretisations-int(np.ceil(b_s_local/b2 * n_discretisations))-int(np.ceil((b_w2-b_s_local)/b2 * n_discretisations))):
        cl_yi = cl_alpha_p*alpha_tip
        c_yi = c_p
        alpha_yi = alpha_tip #deg 
        S_yi = dyi_p * c_yi
        correctional_factor_for_lift = A*yi**6 + B *yi**5 + C*yi**4 + D *yi**3 + E*yi**2 + F*yi +G  #numbers from xflr5 comparing 2d to 3d case of straight wing
        local_param = cl_yi* 1/2 *rho * V**2 * c_yi * (correctional_factor_for_lift)
        local_ideal = gamma0 * rho * V* np.sqrt(1-(2*yi/b_total)**2) 
        
        if not final:
            diffs.append((local_param-local_ideal)**2)
        else:
            cls.append(S_yi)
            lifts.append(local_param)
            ys.append(yi)
            ideals.append(local_ideal)
            cs.append(c_yi)
            angles.append(alpha_yi)

    total_diff = sum(diffs,0)
    return total_diff, lifts, ideals, cs, angles, cls, ys, alpha_tip + twist_rate * b_w2


d_cr = 0.1
d_b_s = 0.1

root_chords = np.arange(0.2,0.7 + d_cr,d_cr)
b_ss = np.arange(0,1.2 + d_b_s, d_b_s)

def optimisation (c_r, b_s):
    optimised = False
    i,j,k,counter = 0,0,0,0
    while optimised == False and np.abs(i) <= 3 and np.abs(j) <= 3 and np.abs(k) <= 3 and counter <= 10:
        
        current_diff = calculate_lift_distribution(c_r, b_s)[0]
        diff_cr_up = calculate_lift_distribution(c_r + d_cr/4, b_s)[0]
        if c_p > c_r - d_cr/4:
            diff_cr_down = current_diff
            print (c_r)
        else:
            diff_cr_down = calculate_lift_distribution(c_r - d_cr/4, b_s)[0]
        if b_s + d_b_s/4 < b_w2:
            diff_b_s_up = calculate_lift_distribution(c_r, b_s + d_b_s/4)[0]
        else: 
            diff_b_s_up = current_diff
        if b_s - d_b_s/4 > 0:
            diff_b_s_down =  calculate_lift_distribution(c_r, b_s - d_b_s/4)[0]
        else:
            diff_b_s_down = current_diff

        differences = [current_diff, diff_cr_up, diff_cr_down, diff_b_s_up,diff_b_s_down]
        index = differences.index(min(differences))
        if index == 0:
            optimised = True
        elif index == 1:
            c_r += d_cr/4
            i += 1
        elif index == 2:
            c_r -= d_cr/4
            i -= 1
        elif index == 3:
            b_s += d_b_s/4
            k += 1
        else:
            b_s -= d_b_s/4
            k -= 1
        counter += 1

    return [current_diff, c_r, b_s]

results = [] #np.empty((len(root_angles)*len(root_chords)*len(twist_rates),4))

for root_chord in root_chords:
    for b_s in b_ss:
        results.append(optimisation(root_chord, b_s))
    print (root_chord, b_s)
    

results_arr = np.array(results)
min_diff = np.amin(results_arr[:,0])

index = np.where(results_arr[:, 0] == min_diff)[0][0]

c_r, b_s = results_arr[index][1], results_arr[index][2]
print ('completing final results', c_r, b_s)

diffs, lifts, ideals, cs, angles, cls, ys, alpha_root = calculate_lift_distribution(c_r_local=c_r,b_s_local = b_s, final= True)

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


print (c_r, alpha_root, b_s)
