import numpy as np
import pandas as pd
import glob
import os

#%% Make sure right file path for the Design Parameters excel file is used
os.chdir("..")
os.chdir("..")
file_pattern = "Design parameters interface.xlsx"
file_paths = glob.glob("**/" + file_pattern, recursive=True)

# Environment constants
g = 9.80665 # [m/s^2] gravitational acceleration
rho = 1.225 # [kg/m^3] air density
T = 288.15  # [K] temperature

# Design Parameters
df = pd.read_excel(file_paths[0])

# omit all columns except for Symbol in code and Value
df = df.loc[:,['Symbol in code', 'Value']]

# Create ndarray from dataframe
df = df.to_numpy()
df = df.T
df = df.tolist()
df = dict(zip(df[0], df[1]))

# for index, value in df[['Symbol in code', 'Value']].values:
#     locals()[index] = value

