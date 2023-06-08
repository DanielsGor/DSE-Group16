# Based on: Shape and Orifice Optimization of Airbag Systems for UAV Parachute Landing

import numpy as np
import scipy
import matplotlib.pyplot as plt
import pandas as pd

gamma = 1.4
density_a = [1.28, 1.225, 1.127]  # kg/m^3
pressure_a = [101262.784, 101325, 101306.3363]  # Pa
temperature_a = [275.65, 288.15, 313.15]  # K
R = 287  # J/kgK
g = 9.80665  # m/s^2

# DEFINE THESE CONSTANTS
p_bag_init = 101325  # -, initial bag pressure ratio P_bag/P_a, depends on chosen fan, max back pressure
rho_bag_init = 1.225  # -, initial bag pressure ratio P_bag/P_a, depends on chosen fan, max back pressure
initial_velocity = 4.202856172  # m/s, initial velocity of the uav
B2 = 0.7 * 0.15  # m2, upper bag footprint area
B1 = B2 * 1  # m2, bottom bag footprint area
#B1 = 0.8 * 0.4  # m2, upper side bag footprint area
h0 = .5  # m, initial height of the bag
A_or = (0.08/2)**2 * np.pi * 2 # m2, orifice area
M = 7.68  # kg, mass of the UAV

def B_avg(h):
    return (B2 + (B2 - (B2 - B1)/h0 * h)) / 2

def B(h):
    return (B2 - (B2 - B1)/h0 * h)

h = h0
dh_dt = initial_velocity
p_a, T = pressure_a[1], temperature_a[1]
p_bag = p_bag_init

V_t = B_avg(h) * h

m_t = p_bag * V_t / (R * T)

time_steps = np.linspace(0, 2, 1000)  # seconds

delta_t = 1 / len(time_steps)

accel_list = []
time_steppos = []
m_list = []
p_bag_list = []
h_list = []
vel_list = []
bag_force_list = []
gauge_pressure_list = []

for t in time_steps:
    rho_bag = m_t / V_t
    p_bag = ((rho_bag / rho_bag_init) ** (gamma - 1)) ** (gamma / (gamma - 1)) * p_bag_init


    d2h_dt2 = g - (p_bag - p_a) * B(h) / M
    h = h - dh_dt * delta_t - 0.5 * d2h_dt2 * delta_t ** 2
    dh_dt = dh_dt + d2h_dt2 * delta_t


    if h <= 0:
        print('we hit da bottoms at', dh_dt, 'm/s')
        break

    V_t = B_avg(h) * h

    labda = p_a / p_bag

    C_D = -3.8399 * labda ** 6 + 9.4363 * labda ** 5 - 7.2326 * labda ** 4 + 1.6972 * labda ** 3 - 0.2908 * labda ** 2 - 0.013 * labda + 0.8426

    dm_dt = C_D * A_or * p_a * (1 / R / T) ** .5 * ((2 * gamma)/(gamma - 1) * (p_bag_init/p_a)**((gamma - 1)/(gamma))) ** .5 * ((p_bag/p_a)**((gamma - 1)/gamma) - 1) ** .5

    m_t = m_t - dm_dt * delta_t



    #stop if mt is complex
    if np.iscomplex(m_t):
        print('mt is complex')
        print(h)
        print(m_t)
        print(p_a)
        print(p_bag)
        print((p_bag/p_a)**((gamma - 1)/gamma) - 1)
        break

    accel_list.append(d2h_dt2)
    time_steppos.append(t)
    m_list.append(m_t)
    p_bag_list.append(p_bag)
    h_list.append(h)
    vel_list.append(dh_dt)
    bag_force_list.append((p_bag - p_a) * B(h))
    gauge_pressure_list.append(p_bag - p_a)


    if m_t <= 0:
        print('mt is negative')
        break




# plot the h position
#plt.plot(time_steppos, accel_list)
#plt.plot(time_steppos, m_list)
plt.plot(time_steppos, h_list)
plt.xlabel(r't [$s$]')
plt.ylabel(r'Vertical Position [$m$]')
plt.grid()
plt.show()

plt.plot(time_steppos, [p_bag_i - p_a for p_bag_i in p_bag_list])
plt.xlabel(r't [$s$]')
plt.ylabel(r'Gauge Bag Pressure [$Pa$]')
plt.grid()
plt.show()

plt.plot(time_steppos, vel_list)
plt.xlabel(r't [$s$]')
plt.ylabel(r'Velocity [$m/s$]')
plt.grid()
plt.show()


plt.plot(time_steppos, accel_list, label='Acceleration')
plt.plot(time_steppos, [-3.75 * g for i in accel_list], label='Limit')
plt.xlabel(r't [$s$]')
plt.ylabel(r'Acceleration [$m/s^2$]')
plt.grid()
plt.legend()
plt.show()


plt.plot(time_steppos, [-i for i in bag_force_list], label="Airbag Force")
plt.plot(time_steppos, [-M*g for i in range(len(time_steppos))], label="Gravity")
plt.xlabel(r't [$s$]')
plt.ylabel(r'Airbag Force [$N$]')
plt.grid()
plt.legend()
plt.show()