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
    Vs = [V]
    phi = 0
    roll_rate = 0
    t = 0
    while global_yaw_angle < 2*np.pi*(nTurnsTotal-1) - np.pi/2:
        t += dt
        roll_rate += roll_rate2 * dt
        phi += roll_rate* dt
        a_centripetal = np.tan(np.deg2rad(phi)) * m * g
        
        load = np.sqrt(np.arctan(phi+1))
        Vcurrent = np.sqrt(load)* V

        R = Vcurrent**2/a_centripetal
        
        d_circle_angle = Vcurrent/R *dt

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
        Vs.append(Vcurrent)
    
    return time, x, y, phis, roll_rates, Vs

x = [20]

while np.abs(x[-1] - 25) > accuracy:
    roll_rate2_init += (x[-1]-25)/10
    time, x,y,phis, roll_rates, Vs = fun(roll_rate2_init)

max_load = np.sqrt(np.arctan(max(phis))+1)
print(max_load, max(phis))

print ('max load factor:', max_load, '\nmax angle:', max(phis), '\nmax roll rate:', max(roll_rates),'\nRoll acceleration', roll_rate2_init)
plt.plot (x,y)
plt.show()
print(roll_rate2_init)
print(np.deg2rad(max(roll_rates)))

#final results

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
           
plt.plot (x,y, color = '#34A1C7')
plt.plot ([50-xs for xs in x],y, color = '#34A1C7', label = 'Flight path')


plt.legend(facecolor="white", fontsize='12')
plt.xlabel("$ \Delta y_{E} [m]$", fontsize='14')
plt.ylabel("$ \Delta x_{E} [m]$", fontsize='14')
           
plt.show()