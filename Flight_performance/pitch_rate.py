import numpy as np 
import matplotlib.pyplot as plt

#### Constants ####
dt = 0.001 #s
g = 9.81 #m/s2

#### Aircraft ####
LD_plane = 14 #inital guess TODO:to change
glide_angle = np.arctan(1/LD_plane) #rad
global_pitch_angle = glide_angle
climb_angle = 7.85 #deg

m = 7.68 #kg

V = 15.1 #m/s
cl_cruise = 0.4987
rho = 1.225 #kg/m3
S = 1.1 #m2

cD0 = 0.01571
e = 0.7
A = 7.911
cd_cruise = cD0 + cl_cruise**2/(np.pi * A *e)

T_climb = m*g*np.sin(np.deg2rad(climb_angle)) + cd_cruise * S * 0.5 * V**2 * rho

V = np.sqrt(m*g*np.cos(glide_angle)/S * 2/rho * 1/cl_cruise)

x = [0]
y = [0]
global_pitch_angles = [glide_angle]
times = [0]
Vs = [V]
pitch_rates = [0]
iter = 0
Rs = [0]
accs  =[0]
counter = 0


def pitch_dot2 (dt,pitch):
    dot2 = []
    for idx,value in enumerate(pitch[0:-3]):
        dot2.append((pitch[idx + 2] - 2 * pitch[idx + 1] + pitch[idx]) /dt**2)
    return dot2

while global_pitch_angle > np.deg2rad(-climb_angle):
    time = times[-1] + dt
    global_pitch_angle = global_pitch_angles[-1]
    V = Vs[-1]
    a_tangential = (T_climb + m*g * np.sin(global_pitch_angle) - cd_cruise * 0.5 * rho * V**2 * S) / m
    V += a_tangential * dt
    a_centripetal = cl_cruise * 0.5 * rho * V**2 * S/m - g * np.cos(global_pitch_angle)
    R = V**2 / a_centripetal
    Rs.append(R)
    pitch_rates.append(V/R)
    accs.append(a_centripetal)
    d_circle_angle = V/R *dt

    x_n = x[-1] + R * np.sin(global_pitch_angle) - R * np.sin(global_pitch_angle - d_circle_angle)
    y_n = y[-1] + R * np.cos(global_pitch_angle) - R * np.cos(global_pitch_angle - d_circle_angle)

    x.append(x_n)
    y.append(y_n)
    global_pitch_angle -= d_circle_angle
    global_pitch_angles.append(global_pitch_angle)
    times.append(time)
    Vs.append(V)
    counter += 1



Ls = [cl_cruise * 1/2 * rho * Vcurrent ** 2 * S for Vcurrent in Vs]
Ws = m * g / np.cos(global_pitch_angles)
ns = Ls/Ws

# plt.plot(times, ns)
# plt.show()


print ('max load factor:', max(ns), '\nmax pitch rate:', max(pitch_rates),'\nRoll pitch acceleration', max(pitch_dot2(dt,global_pitch_angles)),min(pitch_dot2(dt,global_pitch_angles)))


plt.plot(times[:-3],pitch_dot2(dt,global_pitch_angles))
plt.show()

plt.plot(times,Vs)
plt.show()

plt.plot (x,y)
plt.show()
# plt.plot (x, y)
# plt.show()

#results 


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
           
plt.plot (x,y, color = '#34A1C7', label = 'Flight path')

plt.legend(facecolor="white", fontsize='12')
plt.xlabel("$ \Delta x_{E}[m]$", fontsize='14')
plt.ylabel("$ \Delta z_{E}[m]$", fontsize='14')
           
plt.show()
