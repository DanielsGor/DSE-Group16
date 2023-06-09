import numpy as np
import pandas as pd
import itertools
import matplotlib.pyplot as plt
from preprocessing import get_data_matlab, get_test_matrix, calc_aero_forces
from processing import combine_data, get_coeff, split_data, plotting

#model data
#data for model and force balance
x_ac_to_fb = 0.1 # m distance from aerodynamic center to force balance center
y_ac_fb = 0.1 # m distance from aerodynamic center to force balance center

S = 0.1 # m^2
c = 0.2 # m
rho = 1.225 # kg/m^3
v = 15 # m/s

def main():
    #get data from matlab
    mean_norm, mean_ax = get_data_matlab()

    #get test matrix
    test_matrix = get_test_matrix()

    #calculate aerodynamic forces
    data = calc_aero_forces(test_matrix, mean_norm, mean_ax, x_ac_to_fb, y_ac_fb)

    #combine data from wind tunnel test
    df = combine_data(data, test_matrix)

    #get aerodynamic coefficients
    df = get_coeff(df, S, c, rho, v)

    #split data into test series
    df_1, df_2, df_3, df_4 = split_data(df)
    
    #plot data
    plotting(df_1)
    plotting(df_2)
    plotting(df_3)
    plotting(df_4)

    return
