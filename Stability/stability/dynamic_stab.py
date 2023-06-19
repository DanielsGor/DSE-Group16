import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from constants import S, V, rho


# Longitudinal

# Constants
g = 9.80665  # [m/s^2]
rho = 1.225  # [kg/m^3]
S = 0.578
b = 3
V = 15

# Aircraft parameters
mac = 0.192666666666667  # [m]
V_0 = 15  # [m/s]
mass = 8.86  # [kg] preliminary
I_xx = 5.9564435
I_yy = 2.036054485
I_zz = 2.650582532

# Stability derivatives
mu_b = mass * g/b
muc = mass * g / mac


# find K

K_xx = I_xx  / (rho * S * mac ** 3 * mu_b)
K_yy = I_yy / (rho * S * mac ** 3 * muc)
K_zz = I_zz / (rho * S * mac ** 3 * mu_b)
K_xz = 0  # placeholder


# Row 1
C_X_u = 0.0001846  # placeholder
C_X_a = -0.7877451  # placeholder
C_Z_0 = 1.0309919  # placeholder
C_X_q = 3.0980575  # placeholder

# Row 2
C_Z_u = 0.0028627  # placeholder
C_Z_a = 6.9269736  # placeholder
C_Z_a_dot = 0  # placeholder
C_X_0 = 0.0539141  # placeholder
C_Z_q = 7.7926754  # placeholder

# Row 4
C_m_u = 0.0074638  # placeholder
C_m_a = 4.2850081  # placeholder
C_m_a_dot = 0  # placeholder
C_m_q = -104.6554409  # placeholder

# Control derivatives
C_X_f_upper = 0.35  # placeholder
C_X_f_lower = 0.35  # placeholder
C_X_dc_upper = 0.35  # placeholder
C_X_dc_lower = 0.35  # placeholder
C_X_dt = 0.35  # placeholder
C_Z_f_upper = 0.35  # placeholder
C_Z_f_lower = 0.35  # placeholder
C_Z_dc_upper = 0.35  # placeholder
C_Z_dc_lower = 0.35  # placeholder
C_Z_dt = 0.35  # placeholder
C_m_f_upper = 0.35  # placeholder
C_m_f_lower = 0.35  # placeholder
C_m_dc_upper = 0.35  # placeholder
C_m_dc_lower = 0.35  # placeholder
C_m_dt = 0.35  # placeholder

# PQR form
P_long = np.array([[-2 * muc * mac / V_0, 0, 0, 0],
                  [0, (C_Z_a_dot - 2 * muc) * mac / V_0, 0, 0],
                  [0, 0, -mac / V_0, 0],
                  [0, C_m_a_dot * mac / V_0, 0, -2 * muc * K_yy * mac / V_0]])

Q_long = np.array([[-C_X_u, -C_X_a, -C_Z_0, 0],
                  [-C_Z_u, -C_Z_a, -C_X_0, -C_Z_q - 2 * muc],
                  [0, 0, 0, -1],
                  [-C_m_u, -C_m_a, 0, -C_m_q]])

R_long = np.array([[-C_X_f_upper, -C_X_f_lower, -C_X_dc_upper, -C_X_dc_lower, -C_X_dt],
                  [-C_Z_f_upper, -C_Z_f_lower, -C_Z_dc_upper, -C_Z_dc_lower, -C_Z_dt],
                  [0, 0, 0, 0, 0],
                  [-C_m_f_upper, -C_m_f_lower, -C_m_dc_upper, -C_m_dc_lower, -C_m_dt]])

# State Space Matrices
A_long = np.linalg.inv(P_long) @ Q_long
#B_long = np.linalg.inv(P_long) @ R_long

'''
C_long = np.array([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]])

D_long = np.array([[0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [1, 0, 0, 0, 0],
                   [0, 1, 0, 0, 0],
                   [0, 0, 1, 0, 0],
                   [0, 0, 0, 1, 0],
                   [0, 0, 0, 0, 1]])
'''
# Lateral

# Stability parameters
C_Y_beta = -0.1603275
C_Y_beta_dot = 0  # placeholder
C_L = 0.622  # C_L value of the full plane during operation
C_Y_p = -0.0206750
C_Y_r = 0.1801969
C_l_beta = -0.0040371
C_l_p = -0.7228130
C_l_r = 0.2897336

C_n_beta = 0.0313242
C_n_beta_dot = 0
C_n_p = -0.0792286
C_n_r = -0.0639039

# Control parameters
C_Y_f_a_r = 0.3
C_Y_f_a_l = 0.3
C_Y_f_r_r = 0.3
C_Y_f_r_l = 0.3
C_Y_dc_a_r = 0.3
C_Y_dc_a_l = 0.3
C_Y_dc_r_r = 0.3
C_Y_dc_r_l = 0.3

C_l_f_a_r = 0.3
C_l_f_a_l = 0.3
C_l_f_r_r = 0.3
C_l_f_r_l = 0.3
C_l_dc_a_r = 0.3
C_l_dc_a_l = 0.3
C_l_dc_r_r = 0.3
C_l_dc_r_l = 0.3

C_n_f_a_r = 0.3
C_n_f_a_l = 0.3
C_n_f_r_r = 0.3
C_n_f_r_l = 0.3
C_n_dc_a_r = 0.3
C_n_dc_a_l = 0.3
C_n_dc_r_r = 0.3
C_n_dc_r_l = 0.3


# Lateral state space parameters
P_lat = np.array([[(C_Y_beta_dot - 2 * mu_b) * b / V, 0, 0, 0],
                 [0, -1 / (2 * b / V), 0, 0],
                 [0, 0, -4 * mu_b * K_xx * b / V, 4 * mu_b * K_xz * b / V],
                 [C_n_beta_dot, 0, 4 * mu_b * K_xz * b / V, -4 * mu_b * K_zz * b / V]])
Q_lat = np.array([[-C_Y_beta, -C_L, -C_Y_p, -(C_Y_r - 4 * mu_b)],
                  [0, 0, -1, 0],
                  [-C_l_beta, 0, -C_l_p, -C_l_r],
                  [-C_n_beta, 0, -C_n_p, -C_n_r]])
R_lat = np.array([[-C_Y_f_a_r, -C_Y_f_a_l, -C_Y_f_r_r, -C_Y_f_r_l, -C_Y_dc_a_r, -C_Y_dc_a_l, -C_Y_dc_r_r, -C_Y_dc_r_l],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [-C_l_f_a_r, -C_l_f_a_l, -C_l_f_r_r, -C_l_f_r_l, -C_l_dc_a_r, -C_l_dc_a_l, -C_l_dc_r_r, -C_l_dc_r_l],
                  [-C_n_f_a_r, -C_n_f_a_l, -C_n_f_r_r, -C_n_f_r_l, -C_n_dc_a_r, -C_n_dc_a_l, -C_n_dc_r_r, -C_n_dc_r_l]])

A_lat = np.linalg.inv(P_lat) @ Q_lat
#B_lat = np.linalg.inv(P_lat) @ R_lat
'''
C_lat = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1],
                  [0, 0, 0, 0]])
D_lat = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]])

'''

# Calculate eigenvalues of A matrices
eig_long = np.linalg.eig(A_long)
eig_lat = np.linalg.eig(A_lat)

print(eig_long)
print(eig_lat)

# Plot poles of longitudinal and lateral matrices
plt.figure(1)
plt.plot(eig_long[0].real, eig_long[0].imag, 'x')
plt.plot(eig_lat[0].real, eig_lat[0].imag, 'x')

# indicate eigenmotions of longitudinal and lateral matrices

plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.title('Poles of longitudinal and lateral matrices')
plt.legend(['Longitudinal', 'Lateral'])
plt.grid()
plt.show()
