"""This system assumes the following:
    1. The aircraft is small compared to the turn radius
    2. The angle of attach during a turn remains constant as a consequence of 1
    3. The flow is incompressible
    4. The validity of estimation methods has been previously established under Horizontal Tail Sizing
    5. Velocity is constant over the flight phase
    6. Lift during the steady pull up manoeuver stays constant"""


import numpy as np

from roll_rate import dt, Rs, m
from Stability.Horizontal_tail_sizing_final import deda, VhV2
from Stability.tail_sizing import htail_volume
from pitch_rate import

####Constants####
rho = 1.225
g0 = 9.81 #[m/s2]
V = 15.1

####Plasma####
delta_CL_plasma = 0.06




####Aircraft####
x_cg = 0.5
m = 7.68
theta_dot2 = 0



####Wing####
Cm_ac = -0.16
Cm_ac_h = -0.01
x_w_bar = 0.25
MAC = 0.3
CL_alpha = 0
S = 1.1

n = 1.38



####Tail####
CL_alpha_h = 0

S_h = 0.1175
A_h = 5
MAC_h = np.sqrt(S_h/A_h)

x_np = MAC*(CL_alpha_h/CL_alpha)*(1-deda)*VhV2*htail_volume+x_w_bar

x_bar = x_cg - x_np

S_p = (m*V**2/g0 / (n-1)-0.5*rho*(Cm_ac*S*MAC+VhV2*S_h*MAC_h*Cm_ac_h))/(delta_CL_plasma*x_bar)



