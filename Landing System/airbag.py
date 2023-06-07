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
B2 = 0.7 * 0.15  # m2, lower side bag footprint area
B1 = B2  # m2, upper side bag footprint area
#B1 = 0.8 * 0.4  # m2, upper side bag footprint area
h0 = 20  # m, initial height of the bag
A_or = 0.00000018  # m2, orifice area
M = 7.68  # kg, mass of the UAV

def B_avg(h):
    return (B2 + (B2 - (B2 - B1)/h0 * h)) / 2

def B(h):
    return (B2 - (B2 - B1)/h0 * h)

h = h0
dh_dt = initial_velocity
p_a, T = pressure_a[1], temperature_a[1]
p_bag = p_bag_init

V_t = B2 * h

m_t = p_bag * V_t / (R * T)

time_steps = np.linspace(0, 15, 1000)  # seconds

delta_t = 1 / len(time_steps)

accel_list = []
time_steppos = []
m_list = []
p_bag_list = []
h_list = []
vel_list = []
bag_force_list = []

for t in time_steps:
    rho_bag = m_t / V_t
    p_bag = (rho_bag / rho_bag_init) ** (gamma - 1) ** (gamma / (gamma - 1)) * p_bag_init


    d2h_dt2 = g - (p_bag - p_a) * B(h) / M
    h = h - dh_dt * delta_t - 0.5 * d2h_dt2 * delta_t ** 2
    dh_dt = dh_dt + d2h_dt2 * delta_t

    V_t = B2 * h

    labda = p_a / p_bag

    print(labda)

    C_D = -3.8399 * labda ** 6 + 9.4363 * labda ** 5 - 7.2326 * labda ** 4 + 1.6972 * labda ** 3 - 0.2908 * labda ** 2 - 0.013 * labda + 0.8426

    dm_dt = C_D * A_or * p_a * (1 / R / T) ** .5 * ((2 * gamma)/(gamma - 1) * (p_bag_init/p_a)**((gamma - 1)/(gamma))) ** .5 * ((p_bag/p_a)**((gamma - 1)/gamma) - 1) ** .5

    m_t = m_t - dm_dt * delta_t


    #stop if mt is complex
    if np.iscomplex(m_t):
        break

    accel_list.append(d2h_dt2)
    time_steppos.append(t)
    m_list.append(m_t)
    p_bag_list.append(p_bag)
    h_list.append(h)
    vel_list.append(dh_dt)
    bag_force_list.append((p_bag - p_a) * B(h))


    if m_t <= 0:
        break




# plot the h position
#plt.plot(time_steppos, accel_list)
#plt.plot(time_steppos, m_list)
plt.plot(time_steppos, h_list)
#plt.plot(time_steppos, p_bag_list)
plt.xlabel('time')
plt.ylabel('h(t)')
plt.show()

plt.plot(time_steppos, p_bag_list)
plt.xlabel('time')
plt.ylabel('pressure')
plt.show()

plt.plot(time_steppos, vel_list)
plt.xlabel('time')
plt.ylabel('velocity')
plt.show()


plt.plot(time_steppos, accel_list)
plt.xlabel('time')
plt.ylabel('accel')
plt.show()


plt.plot(time_steppos, bag_force_list, label="bag force")
plt.plot(time_steppos, [M*g for i in range(len(time_steppos))], label="Gravity")
plt.xlabel('time')
plt.ylabel('Newton')
plt.legend()
plt.show()