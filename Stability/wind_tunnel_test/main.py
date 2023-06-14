import numpy as np
import pandas as pd

from preprocessing import calc_aero_forces
from processing import get_coeff, split_data, TestSeries

#model data
#data for model and force balance
x_ac_to_fb = 0.01 # m distance from aerodynamic center to force balance center
y_ac_fb = 0.01 # m distance from aerodynamic center to force balance center

"""
    THESE ARE PRELIMINARY VALUES, CHANGE THEM TO THE CORRECT VALUES
"""

S = 0.1 # m^2
c = 0.2 # m
rho = 1.225 # kg/m^3
v = 15 # m/s

def main():
    #preprocessing
    #data = calc_aero_forces(x_ac_to_fb=x_ac_to_fb, y_ac_fb=y_ac_fb)
    data = pd.read_excel('Stability\\wind_tunnel_test\\data.xlsx') #remember to remove and use above line
    #processing
    data = get_coeff(data, S, c, rho, v)
    #split data into test cases
    df_1, df_3, df_4 = split_data(data)
    test_series1 = TestSeries(name='Test Series 1', measurements=df_1, plot=False)
    test_series3 = TestSeries(name='Test Series 3', measurements=df_3, plot=False)
    test_series4 = TestSeries(name='Test Series 4', measurements=df_4, plot=False)

    #get derivatives
    test_series1.get_derivatives()
    test_series3.get_derivatives()
    test_series4.get_derivatives()
    print('Variable test series 1: ', test_series1.x)
    print('Variable test series 3: ', test_series3.x)
    print('Variable test series 4: ', test_series4.x)

    return

if __name__ == '__main__':
    main()