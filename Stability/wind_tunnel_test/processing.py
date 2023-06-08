import numpy as np
import pandas as pd
import itertools
import matplotlib.pyplot as plt
from preprocessing import calc_aero_forces


def combine_data(data):
    test_matrix = pd.read_excel('Stability\\wind_tunnel_test\\wind_tunnel_test_matrix.xlsx')

    df = pd.concat([test_matrix, data], axis=1)
    return df

def get_coeff(df, S, c, rho, v):
    df['Cl'] = df['L'] / (0.5 * rho * S * v**2)
    df['Cd'] = df['D'] / (0.5 * rho * S * v**2)
    df['Cm'] = df['M'] / (0.5 * rho * S * v**2 * c)
    df.drop(['L', 'D', 'M'], axis=1, inplace=True)
    return df

def split_data(df):
    df_1 = df[df['test series'] == 1]
    df_2 = df[df['test series'] == 2]
    df_3 = df[df['test series'] == 3]
    df_4 = df[df['test series'] == 4]

    return df_1, df_2, df_3, df_4

def plotting(df):
    #get variables used in test series
    alpha_range = list(df['alpha'].drop_duplicates())
    V_pp_range = list(df['V_pp'].drop_duplicates())
    f_burst_range = list(df['f_burst'].drop_duplicates())
    duty_cycle_range = list(df['duty_cycle'].drop_duplicates())

    #find x to plot against
    par_dict = {'alpha': alpha_range, 'V_pp': V_pp_range, 'f_burst': f_burst_range, 'duty_cycle': duty_cycle_range}
    print("Parameter Dict:", par_dict)
    #find longest list in par_dict
    longest_list = max(par_dict, key=lambda k: len(par_dict[k]))
    x = par_dict[longest_list]
    #remove longest list from par_dict
    del par_dict[longest_list]
    
    combinations_list = list(itertools.product(*par_dict.values()))
    combinations_dict = {}
    for i, key in enumerate(par_dict.keys()):
        combinations_dict[key] = [c[i] for c in combinations_list]

    print("Longest list:", longest_list)

    if plot:
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        fig.suptitle('Aerodynamic coefficients vs ' + longest_list)

        #ax1
        ax1.set_title('Cl' + '-' + longest_list)
        for i in range(len(list(combinations_dict.values())[0])):
            y = df[(df[list(combinations_dict.keys())[0]] == list(combinations_dict.values())[0][i]) & (df[list(combinations_dict.keys())[1]] == list(combinations_dict.values())[1][i]) & (df[list(combinations_dict.keys())[2]] == list(combinations_dict.values())[2][i])]['Cl']
            ax1.plot(x, y, label=list(combinations_dict.keys())[0] + ' = ' + str(list(combinations_dict.values())[0][i]) + ', ' + list(combinations_dict.keys())[1] + ' = ' + str(list(combinations_dict.values())[1][i]) + ', ' + list(combinations_dict.keys())[2] + ' = ' + str(list(combinations_dict.values())[2][i]))
        ax1.legend()
        ax1.grid()
        ax1.set_xlabel(longest_list)
        ax1.set_ylabel('Cl')

        #ax2
        ax2.set_title('Cd' + '-' + longest_list)
        for i in range(len(list(combinations_dict.values())[0])):
            y = df[(df[list(combinations_dict.keys())[0]] == list(combinations_dict.values())[0][i]) & (df[list(combinations_dict.keys())[1]] == list(combinations_dict.values())[1][i]) & (df[list(combinations_dict.keys())[2]] == list(combinations_dict.values())[2][i])]['Cd']
            ax2.plot(x, y, label=list(combinations_dict.keys())[0] + ' = ' + str(list(combinations_dict.values())[0][i]) + ', ' + list(combinations_dict.keys())[1] + ' = ' + str(list(combinations_dict.values())[1][i]) + ', ' + list(combinations_dict.keys())[2] + ' = ' + str(list(combinations_dict.values())[2][i]))
        ax2.legend()
        ax2.grid()
        ax2.set_xlabel(longest_list)
        ax2.set_ylabel('Cd')

        #ax3
        ax3.set_title('Cm-' + '-' + longest_list)
        for i in range(len(list(combinations_dict.values())[0])):
            y = df[(df[list(combinations_dict.keys())[0]] == list(combinations_dict.values())[0][i]) & (df[list(combinations_dict.keys())[1]] == list(combinations_dict.values())[1][i]) & (df[list(combinations_dict.keys())[2]] == list(combinations_dict.values())[2][i])]['Cm']
            ax3.plot(x, y, label=list(combinations_dict.keys())[0] + ' = ' + str(list(combinations_dict.values())[0][i]) + ', ' + list(combinations_dict.keys())[1] + ' = ' + str(list(combinations_dict.values())[1][i]) + ', ' + list(combinations_dict.keys())[2] + ' = ' + str(list(combinations_dict.values())[2][i]))
        ax3.legend()
        ax3.grid()
        ax3.set_xlabel(longest_list)
        ax3.set_ylabel('Cm')

        plt.show()

    return


def main():
    df = combine_data()
    df = get_coeff(df, S, c, rho, v)
    df_1, df_2, df_3, df_4 = split_data(df)
    plotting(df_4)

if __name__ == '__main__':
    main()