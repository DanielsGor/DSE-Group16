import numpy as np
import pandas as pd

def get_data_matlab():
    import subprocess

    # Path to the MATLAB executable or runtime
    matlab_executable = 'matlab'  # Replace with the correct MATLAB executable or runtime path

    # Path to the MATLAB script
    matlab_script = "C:\\Users\\louis\\PycharmProjects\\SVV\\B50\\DSE-Group16\\Stability\\wind_tunnel_test\\sample_data\\HighLiftTest_PostProcessFile.m"  # Replace with the path to your MATLAB script

    # Command to run the MATLAB script
    command = [matlab_executable, '-nosplash', '-nodesktop', '-r', f"run('{matlab_script}'); exit;"]

    # Run the MATLAB script
    subprocess.call(command)

    df_test_data = pd.read_excel('C:\\Users\\louis\\PycharmProjects\\SVV\\B50\\DSE-Group16\\Stability\\wind_tunnel_test\\sample_data\\wind_tunnel_measurement_data.xlsx')
    
    return df_test_data

def get_test_matrix():
    test_matrix = pd.read_excel('Stability\\wind_tunnel_test\\wind_tunnel_test_matrix.xlsx')
    return test_matrix

def calc_aero_forces(test_matrix = get_test_matrix(), df_test_data = get_data_matlab(), x_ac_to_fb = 0, y_ac_fb = 0):
    data = pd.concat([test_matrix, df_test_data], axis=1)
    mean_norm = df_test_data['Mean Norm']
    mean_ax = df_test_data['Mean Ax']
    
    aoa = test_matrix['alpha'] * np.pi / 180
    L = mean_norm * np.cos(aoa) - mean_ax * np.sin(aoa)
    D = mean_norm * np.sin(aoa) + mean_ax * np.cos(aoa)
    M = x_ac_to_fb * mean_norm + y_ac_fb * mean_ax
    data = pd.DataFrame({'Lift': L, 'Drag': D, 'Moment': M})

    data = pd.concat([test_matrix, data], axis=1)
    
    return data