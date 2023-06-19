import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy as sp
from matplotlib import cycler
colors = cycler('color',
                ['#165baa', '#d382ec', '#34a1c7',
                 '#f765a3', '#0b1354', '#ffa4b6',
                 '#f2e2aa', '#f9d1d1'])
plt.rc('axes', facecolor='#E9E9E9', edgecolor='none',
       axisbelow=True, grid=True, prop_cycle=colors)
plt.rc('grid', color='w', linestyle='solid')
plt.rc('xtick', direction='out', color='gray')
plt.rc('ytick', direction='out', color='gray')
plt.rc('patch', edgecolor='#E6E6E6')
plt.rc('lines', linewidth=2)
# # --------------------------------------------------
# # Reads measurement data from csv
# # --------------------------------------------------
# u_plasma = np.asarray([])
# y_plasma = np.asarray([])
# with open('Plasma/u-y.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         u_plasma = np.append(u_plasma,float(row['u']))
#         y_plasma = np.append(y_plasma,float(row['y']))


def get_data_from_csv(filename):
# --------------------------------------------------
# Reads cfd data from csv
# --------------------------------------------------
    u_mw = np.asarray([])
    y_mw = np.asarray([])
    filepath = "Plasma/"+filename
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            u_mw = np.append(u_mw,float(row['u']))
            y_mw = np.append(y_mw,float(row['y']))
    return u_mw,y_mw

def normalise(u,y):
# --------------------------------------------------
# normalizes velocity profiles and truncates values after 1% of u_max
# --------------------------------------------------
    u_norm = u/np.max(u)
    for i in range(len(u)-1):
        if u_norm[i]>=0.5 and u_norm[i+1]<0.5:
            y_norm = y/y[i]
        if u_norm[i]>0.01 and u_norm[i+1]<0.01:
            u_norm = u_norm[:i]
            y_norm = y_norm[:i]
            break
    
    return u_norm, y_norm

def momentum_thickness(u,y):
    u_for_integral = u*(1-u)
    return np.trapz(u_for_integral,y)



files_csv = ['plasma-x15-y10-v1.csv','plasma-x15-y10-v2.csv','plasma-x15-y10-v3.csv','plasma-x15-y10-v4.csv','plasma-x15-y10-v5.csv','plasma-x15-y10-v6.csv']


# u_mw,y_mw = get_data_from_csv(files_csv[4])
u_plasma,y_plasma = get_data_from_csv('u_y_experiment.csv')
# u_plasma,y_plasma = normalise(u_plasma,y_plasma)
# u_norm, y_norm = normalise(u_mw,y_mw)    

# mt_plasma = momentum_thickness(u_plasma,y_plasma)
# mt_cfd = momentum_thickness(u_norm,y_norm)
# print("Momentum thickness experiment = ", mt_plasma)
# print("Momentum thickness cfd = ", mt_cfd)
# print("Relative difference = ", (mt_plasma-mt_cfd)/mt_plasma)
# plt.style.use('ggplot')
# plt.plot(u_norm,y_norm,'r')

# plt.axvline(-0.01)
# plt.axvline(0.01)


for file in files_csv:
    u, y = get_data_from_csv(file)
    # u, y = normalise(u,y)
    plt.plot(u,y,label="$Simulation, V_{moving wall} = $"+file[-5]+"[m/s]")

# plt.style.use('ggplot')
plt.plot(u_plasma,y_plasma/1000,'X',mfc='black',mew=0,label="Experimental data")
# plt.grid(which='both')
plt.legend(facecolor="white", fontsize='12')
plt.xlabel('u', fontsize='14')
plt.ylabel('y', fontsize='14')
plt.show()