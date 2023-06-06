# Based on: Shape and Orifice Optimization of Airbag Systems for UAV Parachute Landing

import numpy as np
import scipy
import matplotlib.pyplot as plt
import pandas as pd

gamma = 1.4
density_a = [1.28, 1.127, 1.225]  # kg/m^3
pressure_a = [101262.784, 101288.0544, 101306.3363]  # Pa
temperature_a = [275.65, 288.15, 313.15]  # K
R = 287  # J/kgK
g = 9.80665  # m/s^2

# DEFINE THESE CONSTANTS
P_init = 1  # -, initial bag pressure ratio P_bag/P_a, depends on chosen fan, max back pressure
initial_velocity = 4.202856172  # m/s, initial velocity of the uav
B2 = 0.7 * 0.15  # m2, lower side bag footprint area
B1 = B2  # m2, upper side bag footprint area
#B1 = 0.8 * 0.4  # m2, upper side bag footprint area
h0 = 0.4  # m, initial height of the bag
a = 0.018  # m2, orifice area
M = 7.68  # kg, mass of the UAV

def B_avg(h):
    return (B2 + (B2 - (B2 - B1)/h0 * h)) / 2

def B(h):
    return (B2 - (B2 - B1)/h0 * h)

def Cd(P):
    return 0.9 - 0.3 / P

def rho_bag(rho_a, P_bag, P_a):
    return rho_a * (P_bag / P_a) ** (1 / gamma)

def speed_of_sound(T):
    return np.sqrt(gamma * R * T)

def system(t, y):
    # Define the derivatives
    h, dh_dt, P = y

    d2h_dt2 = -g + (P - 1) * p_a * B(h) / M


    c = speed_of_sound(T)
    dP_dt = (P**(1/gamma) * dh_dt * B(h) - a * Cd(P) * np.sqrt((2 * gamma)/(gamma - 1) * (c**2 / gamma) * (P**(1 - 1/gamma) - 1)))/(B_avg(h) * h/gamma * P ** (1/gamma - 1))

    dy_dt = np.array([
        dh_dt,
        d2h_dt2,
        dP_dt
    ])
    # Return the derivatives
    return dy_dt

y_0 = [h0, initial_velocity, P_init]

p_a, T = pressure_a[0], temperature_a[0]

# Solve the system using odeint
solution = scipy.integrate.solve_ivp(system, [0, 1], y_0, method='RK45', max_step=0.01)

print(solution)


yy = solution.y[0]
tt = solution.t
print(yy)
print(tt)


# plot the h position
plt.plot(tt, yy)
plt.xlabel('time')
plt.ylabel('h(t)')
plt.show()