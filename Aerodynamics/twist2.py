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
n_discretisations = 1000 #m

def calculate_lift_distribution (alpha_root_local, c_r_local,twist_dot):

    #main lifting wing
    L_total_req = m*g
    L_plasma = cl_p * rho * V**2 * S_p2 #1/2 is taken out since its factored out in the twist rate calculation
    twist_dot2 = ((alpha_root_local - alpha_cl0)*b_w2 + b_w2**2/2 * (c_p-c_r_local)/b_w2 * (alpha_root_local-alpha_cl0) - b_w2**2/2 * twist_dot - b_w2 ** 3 /3 * twist_dot * (c_p - c_r_local)/b_w2 - (L_total_req  -L_plasma)/ (rho * V**2 * cl_alpha_w))/ (c_r_local*b_w2**3/3 + b_w2/4 * (c_p - c_r_local)/b_w2)
    
    
    n_w = n_discretisations * np.ceil(b_w2/b2 * 100)/100
    dyi_w = b_w2/n_w #added n_discretisations

    cs = []
    angles = []
    lifts = []
    ys = []
    diffs = []
    ideals = []
    cls = []
    for yi in np.linspace(0,b_w2, int(np.ceil(b_w2/b2 * n_discretisations))):    
        c_yi =  (c_p -c_r_local)*(yi/b_w2) + c_r_local
        S_yi = c_yi * dyi_w

        alpha_yi = alpha_root_local - yi*twist_dot - yi**2 * twist_dot2
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
    for yi in np.linspace (b_w2,b_w2+b_p2,n_discretisations-int(np.ceil(b_w2/b2 * n_discretisations))):
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
    return total_diff, lifts, ideals, cs, angles, cls, ys, twist_dot2

### iteration ###

d_alpha_root = 1
d_cr = 0.2
d_twist_rate = 0.2

root_angles = np.arange(-4,-4+d_alpha_root,d_alpha_root)
root_chords = np.arange(1,1.2 + d_cr,d_cr)
twist_rates = np.arange(-5,2 + d_twist_rate,d_twist_rate)


def optimisation (c_r, alpha_root, twist_rate):
    optimised = False
    i,j,k,counter = 0,0,0,0
    while optimised == False and np.abs(i) <= 2 and np.abs(j) <= 2 and np.abs(k) <= 2 and counter <= 10:
        
        current_diff = calculate_lift_distribution(alpha_root, c_r, twist_rate)[0]
        diff_cr_up = calculate_lift_distribution(alpha_root, c_r + d_cr/2, twist_rate)[0]
        if c_r - d_cr < c_p:
            diff_cr_down = current_diff
        else:
            diff_cr_down = calculate_lift_distribution(alpha_root, c_r - d_cr/2, twist_rate)[0]
        diff_alpha_up = calculate_lift_distribution(alpha_root+d_alpha_root/2, c_r, twist_rate)[0]
        diff_alpha_down = calculate_lift_distribution(alpha_root - d_alpha_root/2, c_r, twist_rate)[0]
        diff_twist_rate_up = calculate_lift_distribution(alpha_root, c_r, twist_rate + d_twist_rate/2)[0]
        diff_twist_rate_down =  calculate_lift_distribution(alpha_root, c_r, twist_rate - d_twist_rate/2)[0]

        differences = [current_diff, diff_cr_up, diff_cr_down, diff_alpha_up, diff_alpha_down, diff_twist_rate_up, diff_twist_rate_down]
        index = differences.index(min(differences))
        if index == 0:
            optimised = True
        elif index == 1:
            c_r += d_cr
            i += 1
        elif index == 2:
            c_r -= d_cr
            i -= 1
        elif index == 3:
            alpha_root += d_alpha_root
            j += 1
        elif index == 4:
            alpha_root -= d_alpha_root
            j -= 1
        elif index == 5:
            twist_rate += d_twist_rate
            k += 1
        else:
            twist_rate -= d_twist_rate
            k -= 1
        counter += 1

    return [current_diff, c_r, alpha_root, twist_rate]

results = [] #np.empty((len(root_angles)*len(root_chords)*len(twist_rates),4))

for root_angle in root_angles:
    for root_chord in root_chords:
        for twist_rate in twist_rates:
            results.append(optimisation(root_chord, root_angle, twist_rate))
        print (root_angle, root_chord, twist_rate)
    

results_arr = np.array(results)
min_diff = np.amin(results_arr[:,0])

index = np.where(results_arr[:, 0] == min_diff)[0][0]

c_r, alpha_root, twist_rate = results_arr[index][1], results_arr[index][2], results_arr[index][3]
print ('completing final results', c_r, alpha_root, twist_rate)

diffs, lifts, ideals, cs, angles, cls, ys, twist_rate2 = calculate_lift_distribution(alpha_root_local=alpha_root, c_r_local=c_r,twist_dot=twist_rate)

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


print (c_r, alpha_root, twist_rate, twist_rate2)
