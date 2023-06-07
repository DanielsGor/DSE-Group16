import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy as sp

# --------------------------------------------------
# Reads measurement data from csv
# --------------------------------------------------
u_plasma = np.asarray([])
y_plasma = np.asarray([])
with open('Plasma/u-y.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        u_plasma = np.append(u_plasma,float(row['u']))
        y_plasma = np.append(y_plasma,float(row['y']))

# --------------------------------------------------
# Reads cfd data from csv
# --------------------------------------------------
u_mw = np.asarray([])
y_mw = np.asarray([])
with open('Plasma/plasma-x15-y10-v5.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        u_mw = np.append(u_mw,float(row['u']))
        y_mw = np.append(y_mw,float(row['y']))

def normalise(u,y):
# --------------------------------------------------
# normalizes velocity profiles and truncates values after 1% of u_max
# --------------------------------------------------
    u_norm = u/np.max(u)
    for i in range(len(u)):
        if u_norm[i]>=0.5 and u_norm[i+1]<0.5:
            y_norm = y/y[i]
        # if u_norm[i]>0.01 and u_norm[i+1]<0.01:
        #     u_norm = u_norm[:i]
        #     y_norm = y_norm[:i]
            break
    
    return u_norm, y_norm

def momentum_thickness(u,y):
    u_for_integral = u*(1-u)
    return np.trapz(u_for_integral,y)




u_norm, y_norm = normalise(u_mw,y_mw)    

mt_plasma = momentum_thickness(u_plasma,y_plasma)
mt_cfd = momentum_thickness(u_norm,y_norm)
print("Momentum thickness experiment = ", mt_plasma)
print("Momentum thickness cfd = ", mt_cfd)
print("Relative difference = ", (mt_plasma-mt_cfd)/mt_plasma)
plt.grid(which='both')
plt.plot(u_norm,y_norm,'r')
plt.plot(u_plasma,y_plasma,'o')
plt.axvline(-0.01)
plt.axvline(0.01)
plt.show()