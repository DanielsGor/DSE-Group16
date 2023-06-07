"""This system assumes the following:
    1. The aircraft is small compared to the turn radius
    2. The angle of attach during a turn remains constant as a consequence of 1
    3. The flow is incompressible
    4. The validity of estimation methods has been previously established under Horizontal Tail Sizing
    5. Velocity is constant over the flight phase
    6. Lift during the steady pull up maneuver stays constant"""

import numpy as np
from pitch_rate import R_min, R_min_index, global_pitch_angles, pitch_dot2, times

####Constants####
rho = 1.225
g0 = 9.81 #[m/s2]
V = 15.1

####Plasma####
delta_CL_plasma = 0.06
delta_Cm_plasma = 0.1
MAC_plasma = 0.11

####Aircraft####
x_cg = -0.7
m = 7.68

####Wing####
Cm_ac = -0.16
Cm_ac_h = -0.01
x_w_bar = 0.25
MAC = 0.37
CL_alpha = 6.161
S = 1.1

####Tail####
htail_volume = 0.359
CL_alpha_h = 0.1*180/np.pi
S_h = 0.1175
A_h = 5
MAC_h = np.sqrt(S_h/A_h)
l_h = htail_volume * S * MAC / MAC_h
print(l_h)

theta_dot2 = pitch_dot2(global_pitch_angles, times, R_min_index)
print(R_min)
S_plasma = (m*R_min**2*theta_dot2)/(0.5*1.225*V**2*(delta_CL_plasma*l_h+delta_Cm_plasma*MAC_plasma))

print("Thetadot2 is:", theta_dot2)
print("The surface of the plasma actuator is:", S_plasma)
