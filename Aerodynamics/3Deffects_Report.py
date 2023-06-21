import numpy as np
import matplotlib.pyplot as plt

xs = [0.0619,0.1854,0.3076,0.4276,0.5448,0.6582,0.7672,0.8709,0.9686,1.0598,1.1436,1.2197,1.2875,1.3464,1.3962,1.4364,1.4668,1.4872,1.4974]

ys = [1,0.998855982,0.99650542,0.992811678,0.987557071,0.980425487,0.970941024,0.958476094,0.942166895,0.920831196,0.892917396,0.856411883,0.808833252,0.747328406,0.669072037,0.572036641,0.45610411,0.324418178,0.190299471]

x_poly = np.linspace(0,1.5,1000)
A,B,C,D,E,F,G = -6.4621, 27.265, -44.064, 33.828, -12.495, 1.9321, 0.9162


y_poly = [i for x in x_poly]

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

plt.xlabel('Length along span [m]', fontsize = '14')
plt.ylabel ('Lift fraction', fontsize = '14')
plt.scatter (xs,ys, label = 'Lift distribution for reference wing')
plt.plot (x_poly, y_poly, label = 'Approximating Polynomial', color = '#d382ec')
plt.xlim((0,1.5))
plt.ylim((0,1.1))

# plt.grid(which='both')
plt.legend(facecolor="white", fontsize='12')

plt.show()
