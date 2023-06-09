import subprocess

# Path to the MATLAB executable or runtime
matlab_executable = 'matlab'  # Replace with the correct MATLAB executable or runtime path

# Path to the MATLAB script
matlab_script = "C:\\Users\\louis\\PycharmProjects\\SVV\\B50\\DSE-Group16\\Stability\\wind_tunnel_test\\sample_data\\HighLiftTest_PostProcessFile.m"  # Replace with the path to your MATLAB script

# Command to run the MATLAB script
command = [matlab_executable, '-nosplash', '-nodesktop', '-r', f"run('{matlab_script}'); exit;"]

# Run the MATLAB script
subprocess.call(command)