import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy as sp

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

u_array = np.asarray(range(len(files_csv)))
C_mu = np.asarray([])
for file in files_csv:
    u, y = get_data_from_csv(file)
    C_mu = np.append(C_mu,J(u,y)/(15.1**2*0.5*1.225*0.1692))

plt.plot(u_array+1,C_mu*100)
# plt.legend()
plt.grid()
plt.show()