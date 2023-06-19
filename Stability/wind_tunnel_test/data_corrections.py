import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


#constants
rho = 1.182
V = 15
S = 0.08208
c = 0.152


# create 1st degree polynomial from 2 points
def create_poly(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return np.poly1d([m, b])

# read in cl_alpha data
df_test_data = pd.read_excel('Stability\\wind_tunnel_test\\cl_alpha.xlsx')
analytical_data = create_poly(0, 0, 5, 0.55)

# scale analytical_data
analytical_data = analytical_data * 0.5 * rho * V**2 * S

# scale test data
df_test_data['y'] = df_test_data['y'] * 0.5 * rho * V**2 * S

# scale test data x-axis to fit analytical data
df_test_data['x'] = df_test_data['x'] * 3 / 10

# plot data
plt.plot(df_test_data['x'], df_test_data['y'], 'o', label='Test Data')
plt.plot(df_test_data['x'], analytical_data(df_test_data['x']), label='Analytical Data')
plt.xlabel('Angle of Attack (deg)')
plt.ylabel('Lift [N]')
plt.title('Lift vs Angle of Attack')
plt.legend()
plt.show()

