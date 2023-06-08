import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy as sp

# --------------------------------------------------
# Reads measurement data from csv
# --------------------------------------------------
u_jet = np.asarray([])
v_mw = np.asarray([])
with open('Plasma/plasma_vel.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        v_mw = np.append(v_mw,float(row['vel']))
        u_jet = np.append(u_jet,float(row['u']))

scaling_fact=((u_jet[-1]-u_jet[0])/(v_mw[-1]-v_mw[0]))

print("u(v) jet @x=15mm = ", scaling_fact)
print("Moving wall velocity relative to u=2.5m/s @ x=15mm = ",2.5/scaling_fact)
plt.plot(v_mw,u_jet,'o')
plt.show()