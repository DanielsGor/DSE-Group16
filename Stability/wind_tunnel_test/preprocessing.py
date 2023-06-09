import numpy as np
import pandas as pd

def get_data_matlab():
    "function to read data using matlab scripts"
    return mean_norm, norm_ax

def get_test_matrix():
    test_matrix = pd.read_excel('Stability\\wind_tunnel_test\\wind_tunnel_test_matrix.xlsx')
    return test_matrix

def calc_aero_forces(test_matrix, mean_norm, mean_ax, x_ac_to_fb = 0, y_ac_fb = 0):
    aoa = test_matrix['alpha'] * np.pi / 180
    L = mean_norm * np.cos(aoa) - mean_ax * np.sin(aoa)
    D = mean_norm * np.sin(aoa) + mean_ax * np.cos(aoa)
    M = x_ac_to_fb * mean_norm + y_ac_fb * mean_ax
    data = pd.DataFrame({'Lift': L, 'Drag': D, 'Moment': M})
    return data