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

def J(u,y):
    return np.trapz(u*u,y)*1.225

C_mu_exp = np.asarray([])
V_pp = np.asarray([])
with open('Plasma/momentum-voltage.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        V_pp = np.append(V_pp,float(row['V_pp']))
        C_mu_exp = np.append(C_mu_exp,float(row['c_mu'])/100)
J_exp = C_mu_exp*15*15*2*1.225*0.225/2


files_csv = ['plasma-x15-y10-v1.csv',
             'plasma-x15-y10-v2.csv',
             'plasma-x15-y10-v3.csv',
             'plasma-x15-y10-v4.csv',
             'plasma-x15-y10-v5.csv',
             'plasma-x15-y10-v6.csv',
             'plasma-x15-y10-v7.csv',
             'plasma-x15-y10-v8.csv',
             'plasma-x15-y10-v9.csv',
             'plasma-x15-y10-v10.csv']

u_plasma,y_plasma = get_data_from_csv('u_y_experiment.csv')

u_array = np.asarray(range(len(files_csv)+1))
J_sim = np.asarray([0])
for file in files_csv:
    u, y = get_data_from_csv(file)
    # C_mu = np.append(C_mu,J(u,y)/(15.1**2*0.5*1.225*0.1692))
    J_sim = np.append(J_sim,J(u,y))#*1.345767719100536)

# plt.style.use('ggplot')

print("J for plasma = ",J(u_plasma,y_plasma/1000))
# plt.plot(V_pp,J_exp)
q = np.polyfit(J_sim,u_array,2)
p = np.polyfit(V_pp,J_exp,2)
# plt.plot(V_pp,J_exp)
plt.plot(u_array,J_sim*100)
# plt.plot(V_pp,C_mu_exp*100)
# print(V_pp)
# print(J_exp)
# print(u_array)
# print(J_sim)
print(np.poly1d(p)(12))
# p = np.poly1d([2.45983381e-03, 9.85037659e-01, 1.53444040e+01])
# plt.plot(V_pp,p(V_pp))
# plt.legend()
# plt.grid()
plt.xlabel('Moving wall velocity [m/s]', fontsize='14')
plt.ylabel('$J$ [kg/s$^2$]', fontsize='14')
plt.show()