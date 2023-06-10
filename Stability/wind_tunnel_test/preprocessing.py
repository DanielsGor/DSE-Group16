import numpy as np
import pandas as pd
import subprocess
import glob
import time
import os
def get_data_matlab():
    script_path = glob.glob("**\\HighLiftTest_PostProcessFile.m", recursive=True)[0]
    print(script_path)

    # Path to the MATLAB executable or runtime
    matlab_executable = 'matlab'  # Replace with the correct MATLAB executable or runtime path

    # Path to the MATLAB script
    matlab_script = script_path

    # Command to run the MATLAB script
    command = [matlab_executable, '-nosplash', '-nodesktop', '-r', f"run('{matlab_script}'); exit;"]

    # Run the MATLAB script
    subprocess.call(command)

    pattern = "**/sample_data"    
    directory_path = glob.glob(pattern, recursive=True)[0]

    excel_path = directory_path + '\\wind_tunnel_measurement_data.xlsx'

    while not os.path.exists(excel_path):
        time.sleep(5)


    df_test_data = pd.read_excel(excel_path)
    
    return df_test_data
    


def get_test_matrix():
    path = 'Stability\\wind_tunnel_test\\wind_tunnel_test_matrix.xlsx'
    test_matrix = pd.read_excel('Stability\\wind_tunnel_test\\wind_tunnel_test_matrix.xlsx')
    return test_matrix

def calc_aero_forces(df_test_data, test_matrix, x_ac_to_fb = 0, y_ac_fb = 0):
    data = pd.concat([test_matrix, df_test_data], axis=1)
    mean_norm = df_test_data['Mean Norm']
    mean_ax = df_test_data['Mean Ax']
    
    aoa = test_matrix['alpha'] * np.pi / 180
    L = mean_norm * np.cos(aoa) - mean_ax * np.sin(aoa)
    D = mean_norm * np.sin(aoa) + mean_ax * np.cos(aoa)
    M = x_ac_to_fb * mean_norm + y_ac_fb * mean_ax
    aero_forces = pd.DataFrame({'Lift': L, 'Drag': D, 'Moment': M})

    data = pd.concat([test_matrix, aero_forces], axis=1)
    
    return data


if __name__ == '__main__':
    df_test_data = get_data_matlab()
    print('done')
    test_matrix = get_test_matrix()
    data = calc_aero_forces(df_test_data, test_matrix)
    print('test')
