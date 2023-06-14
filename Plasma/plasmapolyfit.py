import numpy as np
import matplotlib.pyplot as plt
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

p = [ 4.26711683e-05, -3.90262838e-04, -5.98358102e-03]
q = [ 6.25754500e-05,  4.85863752e-04, -1.44483139e-04]
V_pp = np.arange(5,31)

v_mw = (-q[1]+np.sqrt(q[1]**2 - 4*q[0]*(q[2]-p[2]-p[1]*V_pp-p[0]*V_pp**2)))/(2*q[0])
print(v_mw)
plt.plot(V_pp,v_mw)
coef = np.polyfit(V_pp,v_mw,2)
p = np.poly1d(coef)
# plt.plot(V_pp,p(V_pp))
plt.xlabel('$V_{pp}$ [kV]', fontsize='14')
plt.ylabel('Equivalent moving wall velocity [m/s]', fontsize='14')
plt.show()