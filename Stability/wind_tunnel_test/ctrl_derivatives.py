import numpy as np
import pandas as pd
import scipy as sc

#required constants
S = 1
Sh = 1
V_Vh = 1
l_h = 1
mac = 1


#write function to pick out all required derivatives from derivative table for alpha_a, alpha_e, alpha_r
def get_required_derivs_long(alpha_a, alpha_e, alpha_r):
    #get derivatives from table
    #select derivatives from table
    #return derivatives
    return

def calc_ctrl_long():

    C_Z_dc_lower = -Cl_dc*V_Vh*S/Sh
    C_Z_dc_upper = -C_Z_dc_lower
    C_m_dc_lower = C_Z_dc_lower*(l_h/mac)
    C_m_dc_upper = C_Z_dc_upper*(l_h/mac)

    return C_Z_dc_lower, C_Z_dc_upper, C_m_dc_lower, C_m_dc_upper

def calc_ctrl_lat():



    
#write function to account for 3d effects
#write function to convert to actual control derivatives

##Longitudinal control derivatives
C_X_dc_upper = 0
C_X_dc_lower = 0
C_X_dt = 0.35 #placeholder where do we get this from??

C_Z_dt = 0

C_m_dc_upper = 0.35 #placeholder -d Cm/d dc at alpha_e -d Cl/d dc * tail length at alpha_e
C_m_dc_lower = 0.35 #placeholder d Cm/d dc at alpha_e + d Cl/d dc * tail length at alpha_e
C_m_dt = 0


##Lateral control derivatives

C_Y_dc_a_r = 0.3 #placeholder 0?
C_Y_dc_a_l = 0.3 #placeholder 0?
C_Y_dc_r_r = 0.3 #placeholder -d Cl/d dc at alpha_r
C_Y_dc_r_l = 0.3 #placeholder d Cl/d dc at alpha_r

C_l_dc_a_r = 0.3 #placeholder
C_l_dc_a_l = 0.3 #placeholder
C_l_dc_r_r = 0.3 #placeholder 0
C_l_dc_r_l = 0.3 #placeholder 0

C_n_dc_a_r = 0.3 #placeholder 0
C_n_dc_a_l = 0.3 #placeholder 0
C_n_dc_r_r = 0.3 #placeholder
C_n_dc_r_l = 0.3 #placeholder