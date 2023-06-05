import numpy as np 
import matplotlib.pyplot as plt

### inputs ###
LD_plane = 14 #inital guess TODO:to change
glide_angle = np.arctan(1/LD_plane) #rad
global_pitch_angle = glide_angle
climb_angle = 7.85 #deg
g = 9.81 #m/s2
m = 7.68 #kg
dt = 0.001 #s
V = 15.1 #m/s
cl_cruise = 0.92
rho = 1.225 #kg/m3
S = 1.1 #m2

cD0 = 0.01571
e = 0.7
A = 7.911
cd_cruise = cD0 + cl_cruise**2/(np.pi * A *e) 


T_climb = m*g*np.sin(-climb_angle) + cd_cruise * S * 0.5 * V **2 * rho 

x = [0]
y = [0]
global_pitch_angles = [glide_angle]
times = [0]
Vs = [V]
pitch_rates = [0]

while global_pitch_angle > np.deg2rad(-climb_angle):
    time = times[-1] + dt
    global_pitch_angle = global_pitch_angles[-1]
    V = Vs[-1]
    a_tangential= (T_climb + m*g * np.sin(global_pitch_angle) - cd_cruise *0.5 * rho * V**2 * S)/m
    a_centripetal = cl_cruise * 0.5 * rho * V**2 * S/m - g * np.cos (global_pitch_angle)

    R = V**2 / a_centripetal

    pitch_rates.append(V/R)

    d_circle_angle = V/R *dt

    x_n = x[-1] + R * np.sin(global_pitch_angle) - R * np.sin(global_pitch_angle - d_circle_angle)
    y_n = y[-1] + R * np.cos(global_pitch_angle) - R * np.cos(global_pitch_angle - d_circle_angle)

    V += a_tangential * dt

    x.append(x_n)
    y.append(y_n)
    global_pitch_angle -= d_circle_angle
    global_pitch_angles.append(global_pitch_angle)
    times.append(time)
    Vs.append(V)

print (np.mean(pitch_rates), max(pitch_rates))
plt.plot(times, pitch_rates)
#plt.plot (x,y)
plt.show()


