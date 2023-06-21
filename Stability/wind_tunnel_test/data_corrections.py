import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#constants
rho = 1.182
V = 15
S = 0.08208
c = 0.152
h = 0.4
scaler = 0.325
#scaler = 1


# create array of measurement ids
measurement_ids = np.arange(0, 90, 10)
df_test_L_alpha = pd.read_excel('Stability\\wind_tunnel_test\\aero_forces.xlsx')[['id', 'alpha', 'Lift', 'Moment']]
#only take the measurements we want
df_test_L_alpha = df_test_L_alpha[df_test_L_alpha['id'].isin(measurement_ids)]

# correct for open-jet characteristics
sigma = np.pi**2/48 * (c/h)**2
#df_test_L_alpha['effective alpha'] = df_test_L_alpha['alpha'] - (np.sqrt(3*sigma)/np.pi + 2 * sigma/np.pi) * df_test_L_alpha['Lift'] / (0.5 * rho * V**2 * S * c) - sigma/np.pi * df_test_L_alpha['Moment'] / (0.5 * rho * V**2 * S * c**2) 
df_test_L_alpha['effective alpha'] = df_test_L_alpha['alpha'] * scaler

# create 1st degree polynomial from 2 points
def create_poly(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return np.poly1d([m, b])

# read in cl_alpha data

analytical_cl_alpha = create_poly(0, 0, 5, 0.55)


# scale analytical_data
analytical_L_alpha = analytical_cl_alpha * 0.5 * rho * V**2 * S

# scale test data
df_test_cl_alpha = df_test_L_alpha.copy()
df_test_cl_alpha['Lift'] = df_test_cl_alpha['Lift'] / (0.5 * rho * V**2 * S)
df_test_cl_alpha['effective alpha'] = df_test_cl_alpha['alpha'] * scaler



# scale test data x-axis to fit analytical data

# make subplots
fig, ax = plt.subplots(1, 2)

# Plot Lift data and Cl data
ax[0].plot(df_test_L_alpha['effective alpha'], df_test_L_alpha['Lift'], label='Test Data')
ax[0].plot(df_test_L_alpha['effective alpha'], analytical_L_alpha(df_test_L_alpha['effective alpha']), label='Analytical Data')
ax[0].set_xlabel('Angle of Attack (deg)')
ax[0].set_ylabel('Lift [N]')
ax[0].set_title('Lift vs Angle of Attack')
ax[0].legend()

ax[1].plot(df_test_cl_alpha['effective alpha'], df_test_cl_alpha['Lift'], label='Test Data')
ax[1].plot(df_test_cl_alpha['effective alpha'], analytical_cl_alpha(df_test_cl_alpha['effective alpha']), label='Analytical Data')
ax[1].set_xlabel('Angle of Attack (deg)')
ax[1].set_ylabel('Lift Coefficient')
ax[1].set_title('Lift Coefficient vs Angle of Attack')
ax[1].legend()

plt.tight_layout()
plt.show()


