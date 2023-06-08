import numpy as np
import pandas as pd
import itertools
from sample_data_setup import create_dummy_data

#model data
S = 0.1 # m^2
c = 0.2 # m
rho = 1.225 # kg/m^3
v = 15 # m/s

def get_data():
    data = create_dummy_data()
    test_matrix = pd.read_excel('wind_tunnel_test_matrix.xlsx')

    df = pd.concat([test_matrix, data], axis=1)
    return df

def get_coeff(df, S, c, rho, v):
    df['Cl'] = df['L'] / (0.5 * rho * S * v**2)
    df['Cd'] = df['D'] / (0.5 * rho * S * v**2)
    df['Cm'] = df['M'] / (0.5 * rho * S * v**2 * c)
    df.drop(['L', 'D', 'M'], axis=1, inplace=True)
    return df

def split_data(df):
    df_1 = df[df['test_series'] == 1]
    df_2 = df[df['test_series'] == 2]
    df_3 = df[df['test_series'] == 3]
    df_4 = df[df['test_series'] == 4]

    return df_1, df_2, df_3, df_4

def plotting(df):
    #split up into further dataframes
    alpha_range = df['alpha'].unique()
    V_pp_range = df['V_pp'].unique()
    f_burst_range = df['f_burst'].unique()
    duty_cycle_range = df['duty_cycle'].unique()



def main():
    df = get_data()
    df = get_coeff(df, S, c, rho, v)
    df_1, df_2, df_3, df_4 = split_data(df)

if __name__ == '__main__':
    main()