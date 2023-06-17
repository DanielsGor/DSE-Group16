import numpy as np
import pandas as pd
import scipy as sc
import itertools
from matplotlib import cycler
import matplotlib.pyplot as plt
from preprocessing import calc_aero_forces, get_test_matrix

# Plotting settings
colors = cycler('color',
                ['#165baa', '#d382ec', '#34a1c7',
                 '#f765a3', '#0b1354', '#ffa4b6',
                 '#f2e2aa', '#f9d1d1'])
plt.rc('axes', facecolor='#E9E9E9', edgecolor='none',
       axisbelow=True, grid=True)
plt.rc('grid', color='w', linestyle='solid')
plt.rc('xtick', direction='out', color='gray')
plt.rc('ytick', direction='out', color='gray')
plt.rc('patch', edgecolor='#E6E6E6')
#plt.rc('lines', linewidth=2)


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
        self.combinations_list, self.x, self.longest_list, self.keys = self.get_combinations()
        if str('X') in self.x:
            self.x.remove('X')
            print("Removed X from x")
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
        print("Combinations List:", combinations_list)
        keys = list(par_dict.keys())
        '''
        combinations_dict = {}
        for i, key in enumerate(par_dict.keys()):
            combinations_dict[key] = [c[i] for c in combinations_list]
        
        for key in combinations_dict:
            seen = []
            combinations_dict[key] = [x for x in combinations_dict[key] if x not in seen and not seen.append(x)]
        print("Longest list:", longest_list)
        print("Combinations Dict:", combinations_dict)

        '''
        return combinations_list, x, longest_list, keys  

    def plotting(self):

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        fig.suptitle('Aerodynamic coefficients vs ' + self.longest_list)
        #ax1
        ax1.set_title('Cl' + '-' + self.longest_list)
        for i in range(len(self.combinations_list)):
            y = self.measurements[(self.measurements[self.keys[0]] == self.combinations_list[i][0]) & (self.measurements[self.keys[1]] == self.combinations_list[i][1]) & (self.measurements[self.keys[2]] == self.combinations_list[i][2])]['Cl']
            label=self.keys[0] + ' = ' + str(self.combinations_list[i][0]) + ', ' + self.keys[1] + ' = ' + str(self.combinations_list[i][1]) + ', ' + self.keys[2] + ' = ' + str(self.combinations_list[i][2])
            if len(self.x) == len(y):
                ax1.plot(self.x, y, label=label)
            else:
                print('Skipped Cl vs ' + self.longest_list + ' for ' +  self.keys[0] + ' = ' + str(self.combinations_list[i][0]) + ', ' + self.keys[1] + ' = ' + str(self.combinations_list[i][1]) + ', ' + self.keys[2] + ' = ' + str(self.combinations_list[i][2]))
        #ax1.legend(facecolor="white", fontsize='12')
        #ax1.grid(which='both')
        ax1.set_xlabel(self.longest_list, fontsize='14')
        ax1.set_ylabel('Cl', fontsize='14')

        #ax2
        ax2.set_title('Cd' + '-' + self.longest_list)
        for i in range(len(self.combinations_list)): #range(len(list(self.combinations_dict.values())[0])):
            y = self.measurements[(self.measurements[self.keys[0]] == self.combinations_list[i][0]) & (self.measurements[self.keys[1]] == self.combinations_list[i][1]) & (self.measurements[self.keys[2]] == self.combinations_list[i][2])]['Cd']
            if len(self.x) == len(y):
                ax2.plot(self.x, y, label=self.keys[0] + ' = ' + str(self.combinations_list[i][0]) + ', ' + self.keys[1] + ' = ' + str(self.combinations_list[i][1]) + ', ' + self.keys[2] + ' = ' + str(self.combinations_list[i][2]))
            else:
                print('Skipped Cd vs ' + self.longest_list + ' for ' +  self.keys[0] + ' = ' + str(self.combinations_list[i][0]) + ', ' + self.keys[1] + ' = ' + str(self.combinations_list[i][1]) + ', ' + self.keys[2] + ' = ' + str(self.combinations_list[i][2]))
        #ax2.legend(facecolor="white", fontsize='12')
        #ax2.grid(which='both')
        ax2.set_xlabel(self.longest_list, fontsize='14')
        ax2.set_ylabel('Cd', fontsize='14')

        #ax3
        ax3.set_title('Cm-' + '-' + self.longest_list)
        for i in range(len(self.combinations_list)):#range(len(list(self.combinations_dict.values())[0])):
            y = self.measurements[(self.measurements[self.keys[0]] == self.combinations_list[i][0]) & (self.measurements[self.keys[1]] == self.combinations_list[i][1]) & (self.measurements[self.keys[2]] == self.combinations_list[i][2])]['Cm']
            if len(self.x) == len(y):
                ax3.plot(self.x, y, label=self.keys[0] + ' = ' + str(self.combinations_list[i][0]) + ', ' + self.keys[1] + ' = ' + str(self.combinations_list[i][1]) + ', ' + self.keys[2] + ' = ' + str(self.combinations_list[i][2]))
            else:
                print('Skipped Cm vs ' + self.longest_list + ' for ' +  self.keys[0] + ' = ' + str(self.combinations_list[i][0]) + ', ' + self.keys[1] + ' = ' + str(self.combinations_list[i][1]) + ', ' + self.keys[2] + ' = ' + str(self.combinations_list[i][2]))
        #ax3.legend(facecolor="white", fontsize='12')
        #ax3.grid(which='both')
        ax3.set_xlabel(self.longest_list, fontsize='14')
        ax3.set_ylabel('Cm', fontsize='14')


        # Create legend for all subplots
        handles, labels = ax1.get_legend_handles_labels()
        legend_fig = plt.figure()
        plt.legend(handles, labels, loc='upper left', fontsize='12')
        plt.show()

        if self.name=='Test Series 1':
            fig2, ax1 = plt.subplots(1, 1)
            fig2.suptitle('Aerodynamic coefficients vs ' + self.longest_list)
            # ax1
            ax1.set_title('Cl' + '-' + self.longest_list)

            first_curve = None  # Variable to store the first curve

            for i in range(len(self.combinations_list)):
                y = self.measurements[(self.measurements[self.keys[0]] == self.combinations_list[i][0]) & (self.measurements[self.keys[1]] == self.combinations_list[i][1]) & (self.measurements[self.keys[2]] == self.combinations_list[i][2])]['Cl']
                label = self.keys[0] + ' = ' + str(self.combinations_list[i][0]) + ', ' + self.keys[1] + ' = ' + str(self.combinations_list[i][1]) + ', ' + self.keys[2] + ' = ' + str(self.combinations_list[i][2])
                
                if len(self.x) == len(y):
                    if first_curve is None:
                        first_curve = y  # Store the first curve
                    delta_cl = y.to_numpy() - first_curve.to_numpy()  # Subtract the first curve from the current curve
                    ax1.plot(self.x, delta_cl, label=label)  # Plot delta C_L
                else:
                    print('Skipped Cl vs ' + self.longest_list + ' for ' + self.keys[0] + ' = ' + str(self.combinations_list[i][0]) + ', ' + self.keys[1] + ' = ' + str(self.combinations_list[i][1]) + ', ' + self.keys[2] + ' = ' + str(self.combinations_list[i][2]))

            # ax1.legend(facecolor="white", fontsize='12')
            # ax1.grid(which='both')
            ax1.set_xlabel(self.longest_list, fontsize='14')
            ax1.set_ylabel('Delta Cl', fontsize='14')

            # Create legend for all subplots
            handles, labels = ax1.get_legend_handles_labels()
            legend_fig = plt.figure()
            plt.legend(handles, labels, loc='upper left', fontsize='12')
            plt.show()

        return

    def get_derivatives(self):
        for i in range(len(self.combinations_list)):
            cl = self.measurements[(self.measurements[self.keys[0]] == self.combinations_list[i][0]) & (self.measurements[self.keys[1]] == self.combinations_list[i][1]) & (self.measurements[self.keys[2]] == self.combinations_list[i][2])]['Cl']
            cd = self.measurements[(self.measurements[self.keys[0]] == self.combinations_list[i][0]) & (self.measurements[self.keys[1]] == self.combinations_list[i][1]) & (self.measurements[self.keys[2]] == self.combinations_list[i][2])]['Cd']
            cm = self.measurements[(self.measurements[self.keys[0]] == self.combinations_list[i][0]) & (self.measurements[self.keys[1]] == self.combinations_list[i][1]) & (self.measurements[self.keys[2]] == self.combinations_list[i][2])]['Cm']
            if len(self.x) == len(cl) == len(cd) == len(cm):
                #take derivative of each measurement to the next
                cl_int = sc.interpolate.CubicSpline(self.x, cl, bc_type='natural', nan_policy='ignore')
                cd_int = sc.interpolate.CubicSpline(self.x, cd, bc_type='natural', nan_policy='ignore')
                cm_int = sc.interpolate.CubicSpline(self.x, cm, bc_type='natural', nan_policy='ignore')
                cl_deriv = cl_int(self.measurements.index, nu=1)
                cd_deriv = cd_int(self.measurements.index, nu=1)
                cm_deriv = cm_int(self.measurements.index, nu=1)
                #add derivative values to dataframe
                self.measurements['Cl Derivative ' + self.keys[0] + ' = ' + str(self.combinations_list[i][0]) + ', ' + self.keys[1] + ' = ' + str(self.combinations_list[i][1]) + ', ' + self.keys[2] + ' = ' + str(self.combinations_list[i][2])] = cl_deriv
                self.measurements['Cd Derivative ' + self.keys[0] + ' = ' + str(self.combinations_list[i][0]) + ', ' + self.keys[1] + ' = ' + str(self.combinations_list[i][1]) + ', ' + self.keys[2] + ' = ' + str(self.combinations_list[i][2])] = cd_deriv
                self.measurements['Cm Derivative ' + self.keys[0] + ' = ' + str(self.combinations_list[i][0]) + ', ' + self.keys[1] + ' = ' + str(self.combinations_list[i][1]) + ', ' + self.keys[2] + ' = ' + str(self.combinations_list[i][2])] = cm_deriv

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