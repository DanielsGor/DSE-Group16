import numpy as np
import pandas as pd
import scipy as sc

#write function to pick out all required derivatives from derivative table for alpha_a, alpha_e, alpha_r

    
#write function to account for 3d effects
#write function to convert to actual control derivatives

##Longitudinal control derivatives
C_X_f_upper = 0.35 #placeholder -d Cd/d f at alpha_e
C_X_f_lower = 0.35 #placeholder d Cd/d f at alpha_e
C_X_dc_upper = 0.35 #placeholder -d Cd/d dc at alpha_e
C_X_dc_lower = 0.35 #placeholder d Cd/d dc at alpha_e
C_X_dt = 0.35 #placeholder where do we get this from??
C_Z_f_upper = 0.35 #placeholder -d Cl/d f at alpha_e
C_Z_f_lower = 0.35 #placeholder d Cl/d f at alpha_e
C_Z_dc_upper = 0.35 #placeholder -d Cl/d dc at alpha_e
C_Z_dc_lower = 0.35 #placeholder d Cl/d dc at alpha_e
C_Z_dt = 0.35 #placeholder where do we get this from??
C_m_f_upper = 0.35 #placeholder -d Cm/d f at alpha_e
C_m_f_lower = 0.35 #placeholder d Cm/d f at alpha_e
C_m_dc_upper = 0.35 #placeholder -d Cm/d dc at alpha_e 
C_m_dc_lower = 0.35 #placeholder d Cm/d dc at alpha_e
C_m_dt = 0.35 #placeholder where do we get this from??


##Lateral control derivatives
C_Y_f_a_r = 0.3 #placeholder 
C_Y_f_a_l = 0.3 #placeholder
C_Y_f_r_r = 0.3 #placeholder -d Cl/d f at alpha_r
C_Y_f_r_l = 0.3 #placeholder d Cl/d f at alpha_r
C_Y_dc_a_r = 0.3 #placeholder
C_Y_dc_a_l = 0.3 #placeholder
C_Y_dc_r_r = 0.3 #placeholder -d Cl/d dc at alpha_r
C_Y_dc_r_l = 0.3 #placeholder d Cl/d dc at alpha_r

C_l_f_a_r = 0.3 #placeholder
C_l_f_a_l = 0.3 #placeholder
C_l_f_r_r = 0.3 #placeholder 
C_l_f_r_l = 0.3 #placeholder
C_l_dc_a_r = 0.3 #placeholder
C_l_dc_a_l = 0.3 #placeholder
C_l_dc_r_r = 0.3 #placeholder
C_l_dc_r_l = 0.3 #placeholder

C_n_f_a_r = 0.3 #placeholder
C_n_f_a_l = 0.3 #placeholder
C_n_f_r_r = 0.3 #placeholder
C_n_f_r_l = 0.3 #placeholder
C_n_dc_a_r = 0.3 #placeholder
C_n_dc_a_l = 0.3 #placeholder
C_n_dc_r_r = 0.3 #placeholder
C_n_dc_r_l = 0.3 #placeholder