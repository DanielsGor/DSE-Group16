import numpy as np
import pandas as pd
import itertools
import matplotlib.pyplot as plt
from preprocessing import calc_aero_forces, get_test_matrix


def get_data():

    df = calc_aero_forces()
    return df

def get_coeff(df, S, c, rho, v):
    df['Cl'] = df['Lift'] / (0.5 * rho * S * v**2)
    df['Cd'] = df['Drag'] / (0.5 * rho * S * v**2)
    df['Cm'] = df['Moment'] / (0.5 * rho * S * v**2 * c)
    df.drop(['Lift', 'Drag', 'Moment'], axis=1, inplace=True)
    return df

def split_data(df):
    df_1 = df[df['test series'] == 1]
    df_3 = df[df['test series'] == 3]
    df_4 = df[df['test series'] == 4]

    return df_1, df_3, df_4

class TestSeries:
    """A class to represent a test series."""

    def __init__(self, name = str, measurements = pd.DataFrame, plot = False):
        self.name = name
        self.measurements = measurements
        self.combinations_dict, self.x, self.longest_list = self.get_combinations()
        if plot:
            self.plotting()


    def get_name(self):
        return self.name

    def get_measurements(self):
        return self.measurements
    

    def get_combinations(self):
        #get variables used in test series
        alpha_range = list(self.measurements['alpha'].drop_duplicates())
        V_pp_range = list(self.measurements['V_pp'].drop_duplicates())
        f_burst_range = list(self.measurements['f_burst'].drop_duplicates())
        duty_cycle_range = list(self.measurements['duty_cycle'].drop_duplicates())

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

        return combinations_dict, x, longest_list  

    def plotting(self):

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        fig.suptitle('Aerodynamic coefficients vs ' + self.longest_list)
        #ax1
        ax1.set_title('Cl' + '-' + self.longest_list)
        for i in range(len(list(self.combinations_dict.keys())[0])):
            debug_V_pp = list(self.combinations_dict.values())[0][i]
            debug_f_burst = list(self.combinations_dict.values())[1][i]
            debug_duty_cycle = list(self.combinations_dict.values())[2][i]
            y = self.measurements[(self.measurements[list(self.combinations_dict.keys())[0]] == list(self.combinations_dict.values())[0][i]) & (self.measurements[list(self.combinations_dict.keys())[1]] == list(self.combinations_dict.values())[1][i]) & (self.measurements[list(self.combinations_dict.keys())[2]] == list(self.combinations_dict.values())[2][i])]['Cl']
            ax1.plot(self.x, y, label=list(self.combinations_dict.keys())[0] + ' = ' + str(list(self.combinations_dict.values())[0][i]) + ', ' + list(self.combinations_dict.keys())[1] + ' = ' + str(list(self.combinations_dict.values())[1][i]) + ', ' + list(self.combinations_dict.keys())[2] + ' = ' + str(list(self.combinations_dict.values())[2][i]))
        #ax1.legend()
        ax1.grid()
        ax1.set_xlabel(self.longest_list)
        ax1.set_ylabel('Cl')

        #ax2
        ax2.set_title('Cd' + '-' + self.longest_list)
        for i in range(len(list(self.combinations_dict.values())[0])):
            y = self.measurements[(self.measurements[list(self.combinations_dict.keys())[0]] == list(self.combinations_dict.values())[0][i]) & (self.measurements[list(self.combinations_dict.keys())[1]] == list(self.combinations_dict.values())[1][i]) & (self.measurements[list(self.combinations_dict.keys())[2]] == list(self.combinations_dict.values())[2][i])]['Cd']
            ax2.plot(self.x, y, label=list(self.combinations_dict.keys())[0] + ' = ' + str(list(self.combinations_dict.values())[0][i]) + ', ' + list(self.combinations_dict.keys())[1] + ' = ' + str(list(self.combinations_dict.values())[1][i]) + ', ' + list(self.combinations_dict.keys())[2] + ' = ' + str(list(self.combinations_dict.values())[2][i]))
        #ax2.legend()
        ax2.grid()
        ax2.set_xlabel(self.longest_list)
        ax2.set_ylabel('Cd')

        #ax3
        ax3.set_title('Cm-' + '-' + self.longest_list)
        for i in range(len(list(self.combinations_dict.values())[0])):
            y = self.measurements[(self.measurements[list(self.combinations_dict.keys())[0]] == list(self.combinations_dict.values())[0][i]) & (self.measurements[list(self.combinations_dict.keys())[1]] == list(self.combinations_dict.values())[1][i]) & (self.measurements[list(self.combinations_dict.keys())[2]] == list(self.combinations_dict.values())[2][i])]['Cm']
            ax3.plot(self.x, y, label=list(self.combinations_dict.keys())[0] + ' = ' + str(list(self.combinations_dict.values())[0][i]) + ', ' + list(self.combinations_dict.keys())[1] + ' = ' + str(list(self.combinations_dict.values())[1][i]) + ', ' + list(self.combinations_dict.keys())[2] + ' = ' + str(list(self.combinations_dict.values())[2][i]))
        #ax3.legend()
        ax3.grid()
        ax3.set_xlabel(self.longest_list)
        ax3.set_ylabel('Cm')

        plt.show()

        return

    def get_derivatives(self):
        for i in range(len(list(self.combinations_dict.values())[0])):
            cl = self.measurements[(self.measurements[list(self.combinations_dict.keys())[0]] == list(self.combinations_dict.values())[0][i]) & (self.measurements[list(self.combinations_dict.keys())[1]] == list(self.combinations_dict.values())[1][i]) & (self.measurements[list(self.combinations_dict.keys())[2]] == list(self.combinations_dict.values())[2][i])]['Cl']
            cd = self.measurements[(self.measurements[list(self.combinations_dict.keys())[0]] == list(self.combinations_dict.values())[0][i]) & (self.measurements[list(self.combinations_dict.keys())[1]] == list(self.combinations_dict.values())[1][i]) & (self.measurements[list(self.combinations_dict.keys())[2]] == list(self.combinations_dict.values())[2][i])]['Cd']
            cm = self.measurements[(self.measurements[list(self.combinations_dict.keys())[0]] == list(self.combinations_dict.values())[0][i]) & (self.measurements[list(self.combinations_dict.keys())[1]] == list(self.combinations_dict.values())[1][i]) & (self.measurements[list(self.combinations_dict.keys())[2]] == list(self.combinations_dict.values())[2][i])]['Cm']
            #take derivative of each measurement to the next
            cl_derivative = cl.diff()/self.x.diff()
            cd_derivative = cd.diff()/self.x.diff()
            cm_derivative = cm.diff()/self.x.diff()
            self.measurements['Cl Derivative ' + list(self.combinations_dict.keys())[0] + ' = ' + str(list(self.combinations_dict.values())[0][i]) + ', ' + list(self.combinations_dict.keys())[1] + ' = ' + str(list(self.combinations_dict.values())[1][i]) + ', ' + list(self.combinations_dict.keys())[2] + ' = ' + str(list(self.combinations_dict.values())[2][i])] = cl_derivative
            self.measurements['Cd Derivative ' + list(self.combinations_dict.keys())[0] + ' = ' + str(list(self.combinations_dict.values())[0][i]) + ', ' + list(self.combinations_dict.keys())[1] + ' = ' + str(list(self.combinations_dict.values())[1][i]) + ', ' + list(self.combinations_dict.keys())[2] + ' = ' + str(list(self.combinations_dict.values())[2][i])] = cd_derivative
            self.measurements['Cm Derivative ' + list(self.combinations_dict.keys())[0] + ' = ' + str(list(self.combinations_dict.values())[0][i]) + ', ' + list(self.combinations_dict.keys())[1] + ' = ' + str(list(self.combinations_dict.values())[1][i]) + ', ' + list(self.combinations_dict.keys())[2] + ' = ' + str(list(self.combinations_dict.values())[2][i])] = cm_derivative
            
        return

def main():
    """
    THESE ARE PRELIMINARY VALUES, CHANGE THEM TO THE CORRECT VALUES
    """
    S = 1
    c = 0.2
    rho = 1.225
    v = 15


    df = get_data()
    df = get_coeff(df, S, c, rho, v)
    df_1, df_3, df_4 = split_data(df)
    test_series1 = TestSeries(df_1, 'Test Series 1')
    test_series3 = TestSeries(df_3, 'Test Series 3')
    test_series4 = TestSeries(df_4, 'Test Series 4')

if __name__ == '__main__':
    main()