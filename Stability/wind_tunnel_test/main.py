import numpy as np
import pandas as pd
from preprocessing import calc_aero_forces
from processing import get_coeff, split_data, TestSeries

#model data
#data for model and force balance
x_ac_to_fb = 0.050 # m distance from aerodynamic center to force balance center
y_ac_fb = 0.085 - 0.038 # m distance from aerodynamic center to force balance center

S = 0.08208 # m^2
c = 0.152 # m
rho = 1.182 # kg/m^3
v = 15 # m/s

def main():
    #preprocessing
    data = calc_aero_forces(x_ac_to_fb=x_ac_to_fb, y_ac_fb=y_ac_fb)
    #data = pd.read_excel('Stability\\wind_tunnel_test\\data.xlsx') #remember to remove and use above line
    #processing
    data = get_coeff(data, S, c, rho, v)
    data['alpha'] = data['alpha'] * 0.325 #scale alpha to match analytical data
    #split data into test cases
    df_1, df_3, df_4 = split_data(data)
    test_series1 = TestSeries(name='Test Series 1', measurements=df_1, plot=True)
    test_series3 = TestSeries(name='Test Series 3', measurements=df_3, plot=True)
    test_series4 = TestSeries(name='Test Series 4', measurements=df_4, plot=True)
    test_series5 = TestSeries(name='Test Series 5', measurements=df_1, plot=True)

    print('Variable test series 1: ', test_series1.x)
    print('Variable test series 3: ', test_series3.x)
    print('Variable test series 4: ', test_series4.x)

    #get derivatives
    test_series1.get_derivatives()
    test_series3.get_derivatives()
    test_series4.get_derivatives()

    return

if __name__ == '__main__':
    main()