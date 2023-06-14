import numpy as np
import matplotlib.pyplot as plt

rho = 1.225
E = 0.7
W = 7.68 * 9.81
c_D0 = 0.011 * 1.3
V_wind = 3.4
c_lmax = 1.6
Re = 450000
b = 2.95
mu = 1.48e-5

S = np.linspace(0,2,2000)

V_range = (4 * W**2 / (c_D0 * rho **2 * np.pi * b**2 * E* S))**0.25
V_endurance = (4/3 * W**2 / (c_D0 * rho **2 * np.pi * b**2 * E * S) ) ** 0.25
V_Re =  Re * mu * b /(S * rho)
V_c = V_wind + 1.3 * np.sqrt(W/S * 2/rho * 1/c_lmax)

plt.plot (V_endurance, S, color = '#F765A3', linewidth =  3, label = 'Endurance optimised flight', linestyle = '--')
plt.plot (V_range, S, color = '#D382EC', linewidth =  3, label ='Range optimised flight')

plt.fill_betweenx(S,30,V_Re, alpha = 0.3, color = '#165BAA', label = 'Reynolds Limit', linewidth = 0) #hatch = '/', linewidth= 0)
plt.fill_betweenx(S,0,V_c, alpha = 0.3, color = '#34A1C7', label = 'Minimum Velocity', hatch = '\\', linewidth= 0)
plt.xlabel('Velocity [m/s]', fontsize = '14')
plt.ylabel('Surface Area [m]', fontsize = '14')


plt.plot(15.106,1.0617,label = 'Design point', marker="X", markersize=10, markeredgecolor='#0B1354', markerfacecolor='#0B1354')


plt.xlim((13,16))
plt.ylim((0.25,1.75))
plt.legend()
plt.grid(c = 'grey')
plt.show()

