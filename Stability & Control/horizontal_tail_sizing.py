import numpy as np
import matplotlib.pyplot as plt

#functions --------------------------------------------------------------------
#calculate C_L_w_alpha
def calculate_C_L_w_alpha(A, lamda, C_l_alpha):
    E = 1 + 2 * lamda / (A * (1 + lamda))
    C_L_w_alpha = 0.995 * C_l_alpha / (E + C_l_alpha/(np.pi * A))    
    return C_L_w_alpha

#calculate C_L_Ah_alpha
def calculate_C_L_Ah_alpha(C_L_w_alpha, lamda, b, b_fus, c_r, S):
    S_net = S - c_r * b_fus * (1 + lamda/b)/2
    K_i = (1 + 2.15 * b_fus/ b) * S_net/S + np.pi/2 * 1/ C_L_w_alpha * b_fus**2/S
    C_L_Ah_alpha = C_L_w_alpha * K_i
    return C_L_Ah_alpha

#calculate C_L_h_alpha
def calculate_C_L_h_alpha(A_h, lamda_h, C_l_h_alpha):
    E = 1 + 2 * lamda_h / (A_h * (1 + lamda_h))
    C_L_h_alpha = 0.995 * C_l_h_alpha / (E + C_l_h_alpha/(np.pi * A_h))
    return C_L_h_alpha

#constants & inputs -----------------------------------------------------------
#environmental constants
rho = 1.225 # [kg/m^3] air density
g = 9.80665 # [m/s^2] gravitational acceleration
T = 288.15 # [K] temperature

#aircraft constants
m = 7.68 # [kg] aircraft mass
W = m * g # [N] aircraft weight

#cg definitions
x_bar_cg_range = np.linspace(-0.5, 1, 1000) #just for plotting
x_bar_ac = 0.25 # [-] aerodynamic center position aircraft, normalised by mac  #to be adapted once we have the data
x_cg_max_bar = 0.35 # [-] cg max, normalised by mac
x_cg_min_bar = 0.15 # [-] cg min, normalised by mac
delta_x_cg_bar = x_cg_max_bar - x_cg_min_bar # [-] cg range, normalised by mac

#maneuvrability
r = 50 # [m] turn radius
ROC = 5 # [m/s] rate of climb #guessed out of thin air
deltah = 80 # [m] change in altitude for climb
climb_angle = np.arctan(deltah/(np.pi * r)) # [rad] climb angle
v_climb = ROC /np.sin(climb_angle) # [m/s] climb speed

#wing constants
S = 1.1# [m^2] wing surface area
b = 2.95# [m] wing span
b_fus = 0.25 # [m] fuselage width #update asap!
C_l_alpha = 6.161 # [-] lift curve slope airfoil wing
A = b**2 / S # [-] aspect ratio wing
lamda = 0.45 # [-] taper ratio wing
c_r = 0.49078 # [m] root chord wing
mac = 0.37288 # [m] mean aerodynamic chord wing

#horizontal tail constants
A_h = 5 # [-] aspect ratio horizontal tail
lamda_h =  0.8 # [-] taper ratio horizontal tail
C_l_alpha_h = 0.1 * 180/np.pi # [-] lift curve slope horizontal tail airfoil / based on NACA 0012
VhV2 = 1.0 # [-] ratio of horizontal tail velocity to aircraft velocity

#C_L calculations
C_L_h_alpha = calculate_C_L_h_alpha(A_h, lamda_h, C_l_alpha_h)
C_L_w_alpha = calculate_C_L_w_alpha(A, lamda, C_l_alpha)
C_L_Ah_alpha = calculate_C_L_Ah_alpha(C_L_w_alpha, lamda, b, b_fus, c_r, S)
C_L_h = -0.35 * A_h**(1/3) # Lift coefficient of the horizontal tail
C_L_Ah = 2 * W / (rho * v_climb**2 * S) # Lift coefficient of the main wing
C_m_ac = -0.16 # [-]
deda = 0.0 #depends on the tail configuration # formula E-52 in Torenbeek, r and m in fig E-13

# Stability line ----------------------------------------------------------------
SM = 0.05 #stability margin
htail_volume_stability = (x_bar_cg_range - x_bar_ac + SM) / (C_L_h_alpha / C_L_Ah_alpha * (1 - deda) * VhV2)

# Control line ------------------------------------------------------------------
htail_volume_control = 1 / (C_L_h / C_L_Ah * VhV2) * x_bar_cg_range + (C_m_ac / C_L_Ah - x_bar_ac) / (C_L_h / C_L_Ah * VhV2)


#plotting ----------------------------------------------------------------------
plt.plot(x_bar_cg_range, htail_volume_stability, label = 'Stability line')
plt.plot(x_bar_cg_range, htail_volume_control, label = 'Control line')
plt.xlabel('x_cg_bar')
plt.ylabel('Volume_h')
plt.grid()
plt.legend()
plt.show()
