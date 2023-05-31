import numpy as np


#functions

#calculate C_L_w_alpha
def calculate_C_L_w_alpha(A, lamda, C_l_alpha):
    E = 1 + 2 * lamda / (A * (1 + lamda))
    C_L_w_alpha = 0.995 * C_l_alpha / (E + C_l_alpha/(np.pi * A))    
    return C_L_w_alpha

#calculate C_L_Ah_alpha
def calculate_C_L_Ah_alpha(C_L_w_alpha, lamda, b, b_fus, c_root, S):
    S_net = S - c_root * b_fus * (1 + lamda/b)/2
    K_i = (1 + 2.15 * b_fus/ b) * S_net/S + np.pi/2 * 1/ C_L_w_alpha * b_fus**2/S
    C_L_Ah_alpha = C_L_w_alpha * K_i
    return C_L_Ah_alpha

#calculate C_L_h_alpha
def calculate_C_L_h_alpha(A_h, lamda_h, C_l_alpha_h):
    E = 1 + 2 * lamda_h / (A_h * (1 + lamda_h))
    C_L_alpha_h = 0.995 * C_l_alpha_h / (E + C_l_alpha_h/(np.pi * A_h))
    return C_L_h_alpha

#constants & inputs

#wing constants
S = 1.1# [m^2] wing surface area
b = 2.95# [m] wing span
b_fus = # [m] fuselage width
C_l_alpha = # [-] lift curve slope wing
A = 7.91136# [-] aspect ratio wing
lamda = 0.45 # [-] taper ratio wing
c_root = 0.49078# [m] root chord wing
mac = 0.37288 # [m] mean aerodynamic chord wing
VhV2 = 1 # [-] ratio of horizontal tail velocity to aircraft velocity

#horizontal tail constants
A_h = # [-] aspect ratio horizontal tail
lamda_h = # [-] taper ratio horizontal tail
C_l_alpha_h = # [-] lift curve slope horizontal tail


x_bar_cg = 
x_bar_ac =
SM = 0.05 #stability margin

C_L_h_alpha = calculate_C_L_h_alpha(A_h, lamda_h, C_l_alpha_h)
C_L_w_alpha = calculate_C_L_w_alpha(A, lamda, C_l_alpha)
C_L_Ah_alpha = calculate_C_L_Ah_alpha(C_L_w_alpha, lamda, b, b_fus, c_root, S)
C_L_h = #tbd
C_L_Ah = #tbd
C_m_ac =  #to be changed
deda = 0 #to be changed

# Stability line

htail_volume = (x_bar_cg - x_bar_ac + SM) / (C_L_alpha_h / C_L_alpha_Ah * (1 - deda) * VhV2)

# Control line

htail_volume = 1 / (C_L_h / C_L_Ah * VhV2) * x_bar_cg + (C_m_ac / C_L_Ah - x_bar_ac) / (C_L_h / C_L_Ah * VhV2)