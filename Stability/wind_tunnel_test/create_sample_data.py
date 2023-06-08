import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools


def create_dummy_data():
    # create example pandas dataframe
    df_test_matrix = pd.read_excel('Stability\\wind_tunnel_test\\wind_tunnel_test_matrix.xlsx')

    # get the amount of rows in df_test_matrix
    n_tests = df_test_matrix.shape[0]

    df_dummy = pd.DataFrame(columns=['t', 'L', 'D', 'M'])

    # for t create 200 random sample data points between 0  and 10000

    df_dummy['t'] = np.random.randint(0, 10001, n_tests)

    # for L, D, M create 200 random sample data points
    df_dummy['L'] = np.random.randint(-20, 20, n_tests)
    df_dummy['D'] = np.random.randint(-20, 20, n_tests)
    df_dummy['M'] = np.random.randint(-20, 20, n_tests)

    # rank the data by increasing t
    df_dummy = df_dummy.sort_values(by=['t'])
    print('break')
    return df_dummy

create_dummy_data()