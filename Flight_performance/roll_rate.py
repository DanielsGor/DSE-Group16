import numpy as np
import matplotlib.pyplot as plt

### inputs ###
m = 7.68 #kg
g = 9.81 #m/s2
V = 15.1 #m/s
roll_rate = 5 #deg/s
dt = 0.001 #s
t = 0
nTurnsTotal = 2

#TODO: Propulsion influence


#vectors
x = [0] #initialise global position vectors
y = [0] #initialise global position vectors
phis = [0] #deg
time = [t]
Rs = [0] #m
global_yaw_angle = 0
gs = [0] 
phi = 0

while global_yaw_angle < 2*np.pi*(nTurnsTotal-1) - np.pi/2:
    t += dt
    phi += roll_rate* dt
    a_centripetal = np.tan(np.deg2rad(phi)) * m * g
    R = V**2/a_centripetal
    
    d_circle_angle = V/R *dt

    x_n = x[-1] + R * np.cos(global_yaw_angle) - R * (np.cos(global_yaw_angle+d_circle_angle))
    y_n = y[-1] - R * np.sin (global_yaw_angle) + R * (np.sin(global_yaw_angle+d_circle_angle))


    x.append(x_n)
    y.append(y_n)
    time.append(t)
    phis.append(phi)
    Rs.append(R)
    global_yaw_angle += d_circle_angle
    gs.append(global_yaw_angle)

max_load = np.sqrt(np.arctan(max(phis))+1)
print(max_load, max(phis))
print (x[-1],y[-1])
plt.plot (x,y)
plt.show()