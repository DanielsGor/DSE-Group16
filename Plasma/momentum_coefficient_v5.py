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
    return np.trapz(u**2,y)*1.225
files_csv = ['plasma-x9-y10-v5.csv',
             'plasma-x10-y10-v5.csv',
             'plasma-x11-y10-v5.csv',
             'plasma-x12-y10-v5.csv',
             'plasma-x13-y10-v5.csv',
             'plasma-x14-y10-v5.csv',
             'plasma-x15-y10-v5.csv']

u_array = np.asarray(range(len(files_csv)))
C_mu = np.asarray([])
for file in files_csv:
    u, y = get_data_from_csv(file)
    C_mu = np.append(C_mu,J(u,y))#/(15.1**2*0.5*1.225*0.1692))

# plt.style.use('ggplot')

plt.plot((u_array+9),C_mu)
# plt.legend()
# plt.grid()
print(C_mu[1]/C_mu[-1])
plt.xlabel('Location downstream [mm]', fontsize='14')
plt.ylabel('$J$ [kg m/s]', fontsize='14')
plt.show()