import numpy as np
import pandas as pd
import control
from matplotlib import cycler
import matplotlib.pyplot as plt
#from constants import S, V, rho

# Plotting settings
colors = cycler('color',
                ['#165baa', '#d382ec', '#34a1c7',
                 '#f765a3', '#0b1354', '#ffa4b6',
                 '#f2e2aa', '#f9d1d1'])
plt.rc('axes', facecolor='#E9E9E9', edgecolor='none',
       axisbelow=True, grid=True)
plt.rc('grid', color='w', linestyle='solid')
plt.rc('xtick', direction='out', color='gray')
plt.rc('ytick', direction='out', color='gray')
plt.rc('patch', edgecolor='#E6E6E6')

# Longitudinal

# Constants
g = 9.81  # [m/s^2]
rho = 1.225  # [kg/m^3]
S = 0.76
b = 3
V = 15.1

# Aircraft parameters
mac = 0.25333  # [m]
V_0 = 15.1  # [m/s]
mass = 8.86  # [kg] preliminary
I_xx = 3.16189
I_yy = 0.97871
I_zz = 5.90325


# Stability derivatives
mu_b = mass * g / b
muc = mass * g / mac


# find K

K_xx = I_xx  / (rho * S * mac ** 3 * mu_b)
K_yy = I_yy / (rho * S * mac ** 3 * muc)
K_zz = I_zz / (rho * S * mac ** 3 * mu_b)
K_xz = 0  # placeholder

# Row 1
C_X_u = 0.0001311  # placeholder
C_X_a = -0.5742598  # placeholder
C_Z_0 = 0.7764510  # placeholder
C_X_q = 0.4557234  # placeholder

# Row 2
C_Z_u = 0.0021766   # placeholder
C_Z_a = 5.644108  # placeholder
C_Z_a_dot = 0  # placeholder
C_X_0 = 0.0399138  # placeholder
C_Z_q = 9.9805365  # placeholder

# Row 4
C_m_u = 0.0010981  # placeholder
C_m_a = -0.8632242  # placeholder
C_m_a_dot = 0  # placeholder
C_m_q = -32.7477863  # placeholder

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
B_long = np.linalg.inv(P_long) @ R_long
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
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0]])

def short_period():
    #second simplification from slides
    #constant velocity
    #initially steady level flight(gamma=0, theta <<1)
    #ommiting Czadot and Czq (small compared to muc)
    A = 4*(muc**2)*KY2
    B = -2*muc*(KY2*CZa + Cmadot + Cmq)
    C = CZa*Cmq - 2*muc*Cma
    #discriminant:
    D = B**2 -4*A*C
    #abc formula:
    if D >= 0:
        L1 = ((-B+math.sqrt(D))/(2*A))*V0/c
        L2 = ((-B-math.sqrt(D))/(2*A))*V0/c
    else:
        L1 = complex((-B/(2*A)),math.sqrt(-D)/(2 * A))*V0/c
        L2 = complex((-B/(2*A)),-math.sqrt(-D)/(2 * A))*V0/c
    print("lamda_1_short= ", L1)
    print("lamda_2_short= ", L2)


# create state space model
sys_long = control.ss(A_long, B_long, C_long, D_long)

# Define the time vector
t = np.linspace(0, 1000, 1000)

# Set the initial condition for the control variable
initial_condition = np.zeros((sys_long.A.shape[1],))

# Apply an impulse in the desired control variable
initial_condition[1] = 0.1  # Apply the impulse in the first control variable

# Simulate the step response
t_long, y_long = control.initial_response(sys_long, T=t, X0=initial_condition)
'''
y_1 =  y_long[:, 0, :][0]
y_2 =  y_long[:, 0, :][1]
y_3 =  y_long[:, 0, :][2]
y_4 =  y_long[:, 0, :][3]
'''

y_1 = y_long[0]
y_2 = y_long[1]
y_3 = y_long[2]
y_4 = y_long[3]

plt.plot(t_long, y_1, label='u')
plt.plot(t_long, y_2, label='alpha')
plt.plot(t_long, y_3, label='theta')
plt.plot(t_long, y_4, label='q')
plt.legend()
plt.show()




# Lateral

# Stability parameters
C_Y_beta = -0.3449654
C_Y_beta_dot = 0  # placeholder
C_L = 0.82  # C_L value of the full plane during operation
C_Y_p = 0.0690129
C_Y_r = 0.3506571
C_l_beta = 0.0011573
C_l_p = -0.5936046
C_l_r = 0.1985311

C_n_beta = 0.1036754 - 0.0257201
C_n_beta_dot = 0
C_n_p = -0.0719895
C_n_r = -0.1267122

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
B_lat = np.linalg.inv(P_lat) @ R_lat
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

# create state space model
sys_lat = control.ss(A_lat, B_lat, C_lat, D_lat)

# Define the time vector
t = np.linspace(0, 1000, 1000)

# Set the initial condition for the control variable
initial_condition = np.zeros((sys_lat.A.shape[1],))

# Apply an impulse in the desired control variable
initial_condition[2] = 0.01  # Apply the impulse in the first control variable

# Simulate the step response
t_lat, y_lat = control.initial_response(sys_lat, T=t, X0=initial_condition)
'''
y_1 =  y_long[:, 0, :][0]
y_2 =  y_long[:, 0, :][1]
y_3 =  y_long[:, 0, :][2]
y_4 =  y_long[:, 0, :][3]
'''

y_1 = y_lat[0]
y_2 = y_lat[1]
y_3 = y_lat[2]
y_4 = y_lat[3]

plt.plot(t_lat, y_1, label='beta')
plt.plot(t_lat, y_2, label='phi')
plt.plot(t_lat, y_3, label='p')
plt.plot(t_lat, y_4, label='r')
plt.legend()
plt.show()


# Calculate eigenvalues of A matrices
eig_long = np.linalg.eig(A_long)
eig_lat = np.linalg.eig(A_lat)

print(eig_long)
print(eig_lat)

# Plot poles of longitudinal and lateral matrices
plt.plot(eig_long[0].real, eig_long[0].imag, 'x')
plt.plot(eig_lat[0].real, eig_lat[0].imag, 'x')

# indicate eigenmotions of longitudinal and lateral matrices

plt.xlabel('Real')
plt.ylabel('Imaginary')
plt.title('Poles of longitudinal and lateral A-matrices')
plt.legend(['Longitudinal', 'Lateral'])
plt.tight_layout()
plt.show()
