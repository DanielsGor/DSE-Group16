import numpy as np
import matplotlib.pyplot as plt

### inputs ###
roll_rate2_init = 1
droll_rate2 = 0.1
accuracy = 0.1

#TODO: Propulsion influence 

def fun(roll_rate2):
    m = 7.68 #kg
    g = 9.81 #m/s2
    V = 15.1 #m/s
    dt = 0.001 #s
    t = 0
    nTurnsTotal = 2
    #vectors
    x = [0] #initialise global position vectors
    y = [0] #initialise global position vectors
    phis = [0] #deg
    time = [0]
    Rs = [0] #m
    global_yaw_angle = 0
    gs = [0] 
    roll_rates = [0]
    phi = 0
    roll_rate = 0
    t = 0
    while global_yaw_angle < 2*np.pi*(nTurnsTotal-1) - np.pi/2:
        t += dt
        roll_rate += roll_rate2 * dt
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
        roll_rates.append(roll_rate)
    
    return x, y, phis, roll_rates

x = [0]

while np.abs(x[-1] - 25) > accuracy:
    roll_rate2_init += droll_rate2
    x,y,phis, roll_rates = fun(roll_rate2_init)

max_load = np.sqrt(np.arctan(max(phis))+1)
print(max_load, max(phis))
print (x[-1],y[-1])
plt.plot (x,y)
plt.show()
print(roll_rate2_init)
print(np.deg2rad(max(roll_rates)))