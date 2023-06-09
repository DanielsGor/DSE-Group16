import numpy as np
import glob
import pandas as pd
from constants import df
import matplotlib.pyplot as plt
from matplotlib import cycler

class load_distribution:
    def __init__(self, df):
        self.V_cruise = df['V_cruise']  # [m/s] cruise speed
        self.rho = df['rho_atm']  # [kg/m^3] air density
        self.MAC = df['MAC']  # [m] chord
        self.dfF = pd.read_csv(r"C:\Users\oprsc\PycharmProjects\DSE-Group16\Structures\CSV\local_lift_0deg.csv")
        self.coefdist = None
        self.loaddist = None
        self.intload = None
        self.c = None
        self.bigchord = .275
        self.smallchord = 0.169
        self.locbegintaper = 1.1
        self.locendtaper = 1.33
        self.sigma_y = 324  # [MPa] yield stress
        self.UTS = 469  # [MPa] ultimate stress
        self.E = 73.1e3  # [MPa] Young's modulus
        self.tau_str = 283  # [MPa] shear stress
        self.G = 28e3  # [MPa] shear modulus
        self.sigma = None  # [MPa] stress
        self.tau = None  # [MPa] shear stress
        self.qtop = None
        self.qleft = None
        self.qbot = None
        self.qright = None


    def get_array(self):
        # Get rid of all columns except for span and cl and rename them
        # self.dfF = self.dfF.iloc[:, :]
        self.dfF.columns = ['span', 'cl', 'BM', 'cm']
        # Half the dataframe
        self.dfF = self.dfF[self.dfF.iloc[:, 0] > 0]
        # reverse rows of dataframe
        self.dfF = self.dfF.iloc[::-1]

        # Turn dataframe into array and divide by 1000 to get meters
        self.coefdist = np.array(self.dfF)
        self.coefdist[:, 0] = self.coefdist[:, 0]
        # # create load distribution array
        # self.coefdist[:, 0] = self.dfF[:, 0]
        self.c = np.full(len(self.coefdist[self.coefdist[:, 0] >= self.locendtaper]), self.smallchord)
        a = np.linspace(self.smallchord, self.bigchord, len(self.coefdist[self.locbegintaper < self.coefdist[:, 0]]) - len(
            self.coefdist[self.coefdist[:, 0] > self.locendtaper]))
        self.c = np.append(self.c, a)
        self.c = np.append(self.c, np.full(len(self.coefdist[self.coefdist[:, 0] <= self.locbegintaper]), self.bigchord))
        self.c = self.c * 1000
        return self.coefdist, self.c

    # loaddist | span | Lift |
    def get_loaddist(self):
        self.loaddist = np.zeros(self.coefdist.shape)
        self.loaddist[:, 0] = self.coefdist[:, 0]
        for i in range(self.coefdist.shape[0]):
            if i == 0:
                self.loaddist[i, 1] = 0.5 * self.coefdist[i, 1] * self.V_cruise ** 2 * self.rho * self.MAC * (
                            self.coefdist[i, 0] - self.coefdist[i + 1, 0])
            if 1 <= i <= self.coefdist.shape[0] - 2:
                self.loaddist[i, 1] = 0.5 * self.coefdist[i, 1] * self.V_cruise ** 2 * self.rho * self.MAC * (
                            (self.coefdist[i, 0] + self.coefdist[i - 1, 0]) / 2 - (self.coefdist[i, 0] + self.coefdist[i + 1, 0]) / 2)
            if i == self.coefdist.shape[0] - 1:
                self.loaddist[i, 1] = 0.5 * self.coefdist[i, 1] * self.V_cruise ** 2 * self.rho * self.MAC * (self.coefdist[i - 1, 0] - self.coefdist[i, 0])
        self.loaddist[:, 2] = self.coefdist[:, 2]
        return self.loaddist

    # returns internal load array |span|Bending moment|Internal shear|Internal torsion|
    def get_intload(self):
        self.intload = np.zeros((self.coefdist.shape[0], 4))
        self.intload[:, 0] = self.loaddist[:, 0]
        for n in range(self.coefdist.shape[0]):
            self.intload[n, 1] = self.coefdist[n, 2]
            self.intload[n, 2] = -sum(self.loaddist[:n+1, 1])
            if n < self.coefdist.shape[0] - 1:
                if n == 0:
                    self.intload[n, 3] = - self.coefdist[
                        n, 3] * 0.5 * self.rho * self.V_cruise ** 2 * self.MAC * self.c[n]/1000 * (
                                                     self.coefdist[n, 0] - self.coefdist[n + 1, 0]) + self.intload[
                                             n, 1] * 0.2 * self.c[n]/1000
                else:
                    self.intload[n, 3] = self.intload[n-1, 3] - self.coefdist[n, 3] * 0.5 * self.rho * self.V_cruise ** 2 * self.MAC * self.c[n]/1000 * (self.coefdist[n, 0] - self.coefdist[n + 1, 0]) + self.intload[n, 1] * 0.2 * self.c[n]/1000
            elif n == self.coefdist.shape[0] - 1:
                self.intload[n, 3] = self.intload[n-1, 3] - self.coefdist[n, 3] * 0.5 * self.rho * self.V_cruise ** 2 * self.MAC * self.c[n]/1000 * self.coefdist[n, 0] * 2 + self.intload[n, 1] * 0.2 * self.c[n]/1000
        # print(np.abs(np.max(self.intload[:,1])),np.max(np.abs(self.intload[:,2])),np.max(np.abs(self.intload[:,3])))
        return self.intload

    def get_normalstress(self, B1, B2):
        # Ixx for 4 booms of area B [mm^2] each
        Ixxplate = 0.5 * self.c * 0.4 * ((0.085 + 0.045) / 2 * self.c) ** 2
        W = (0.5 * self.c[-1] * 0.4 + 0.5 * (0.085 + 0.045) / 2 * self.c[-1]) * 2 * 1500 * 2710 * 10**(-9)
        # self.Ixx = 2 * B1 * (0.085 * self.c / 2) ** 2 + 2 * B2 * (0.045 * self.c / 2) ** 2 + Ixxplate
        self.Ixx = Ixxplate
        # print(self.intload[:, 1], self.c ,self.Ixx)
        self.sigma = 3.8 * self.intload[:, 1] * 1000 * (0.085 * self.c / 2) / self.Ixx
        # print('sigma',self.sigma,'\n' ,self.sigma_y)
        return self.sigma, self.sigma_y

    def get_shear_stress(self):
        B1 = 15
        B2 = 7
        self.intload[:, 2] = self.intload[:, 2]
        self.intload[:, 3] = self.intload[:, 3] * 1000
        self.qtop = 3.8 * (self.intload[:, 3]/ (2 * (0.085*self.c + 0.045*self.c)/2*0.4*self.c))
        self.qleft = 3.8 * (-self.intload[:, 2] / (2 * 0.085 * self.c) + self.intload[:, 3]/ (2* (0.085*self.c + 0.045*self.c)/2*0.4*self.c))
        self.qbot = 3.8 * (self.intload[:, 3] / (2 * (0.085*self.c + 0.045*self.c)/2*0.4*self.c))
        self.qright = 3.8 * (self.intload[:, 2] / (2 * 0.045 * self.c) + self.intload[:, 3] / (2 * (0.085*self.c + 0.045*self.c)/2*0.4*self.c))
        # print(qtop, qleft, qbot, qright)
        print('qtop',np.max(np.abs(self.qtop/self.tau_str)), 'qleft',np.max(np.abs(self.qleft/self.tau_str)), 'qbot',np.max(np.abs(self.qbot/self.tau_str)), 'qright',np.max(np.abs(self.qright/self.tau_str)), '\n', self.tau_str)
        # print(qtop / 5, qleft / self.tau_str, qbot / 5, qright / self.tau_str)
        # print(self.intload[:,0])

    def plotter(self):
        colors = cycler('color',
                        ['#165baa', '#d382ec', '#34a1c7',
                         '#f765a3', '#0b1354', '#ffa4b6',
                         '#f2e2aa', '#f9d1d1'])
        plt.rc('axes', facecolor='#E9E9E9', edgecolor='none',
               axisbelow=True, grid=True, prop_cycle=colors)
        plt.rc('grid', color='w', linestyle='solid')
        plt.rc('xtick', direction='out', color='gray')
        plt.rc('ytick', direction='out', color='gray')
        plt.rc('patch', edgecolor='#E6E6E6')
        plt.rc('lines', linewidth = 2)
        plt.plot(self.intload[:,0], self.loaddist[:,1], mfc='black', mew=0, label="Torsional moment distribution")
        # plt.grid(which='both')
        plt.legend(facecolor="white", fontsize='12')
        plt.xlabel('Span [m]', fontsize='14')
        plt.ylabel('Torsional Moment [Nmm]', fontsize = '14')
        plt.show()

dist = load_distribution(df)
coefdist, c = dist.get_array()
loaddist = dist.get_loaddist()
intload = dist.get_intload()
sigma, sigma_y = dist.get_normalstress(15,7)
dist.get_shear_stress()
dist.plotter()
# dist.get_shear_stress()
# print(sigma, sigma_y, '\n end')
# # plot load distribution
# # plt.plot(coefdist[:, 0], coefdist[:, 1])
# # plt.plot(loaddist[:, 0], loaddist[:, 1])
# plt.plot(intload[:, 0], intload[:, 1])
# plt.show()



