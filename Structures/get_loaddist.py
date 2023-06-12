import numpy as np
import glob
import pandas as pd
from constants import df
import matplotlib.pyplot as plt

class load_distribution:
    def __init__(self, df):
        self.V_cruise = df['V_cruise']  # [m/s] cruise speed
        self.rho = df['rho_atm']  # [kg/m^3] air density
        self.MAC = df['MAC']  # [m] chord
        self.dfF = pd.read_csv(r"C:\Users\oprsc\PycharmProjects\DSE-Group16\Structures\CSV\Wing_Graph_2.csv")
        self.coefdist = None
        self.loaddist = None
        self.intload = None
        self.c = None
        self.bigchord = .2
        self.smallchord = 0.169
        self.locbegintaper = 0.9
        self.locendtaper = 1.4
        self.sigma_y = 324 # [MPa] yield stress
        self.UTS = 469 # [MPa] ultimate stress
        self.E = 73.1e3 # [MPa] Young's modulus
        self.tau_str = 283 # [MPa] shear stress
        self.G = 28e3 # [MPa] shear modulus
        self.sigma = None # [MPa] stress
        self.tau = None # [MPa] shear stress

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
        # print(self.c)
        return self.coefdist, self.c
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
        self.loaddist[:, 2] = self.loaddist[:, 1]/(48/1.5)
        # print(self.loaddist)
        return self.loaddist

    # returns internal load array |span|Bending moment|Internal shear|Internal torsion|
    def get_intload(self):
        self.intload = np.zeros((self.coefdist.shape[0], 4))
        self.intload[:, 0] = self.loaddist[:, 0]
        for n in range(self.coefdist.shape[0]):
            self.intload[n, 1] = self.coefdist[n, 2]
            self.intload[n, 2] = -sum(self.loaddist[:n+1, 1])
            if n < self.coefdist.shape[0] - 1:
                self.intload[n, 3] = - self.coefdist[n, 3] * 0.5 * self.rho * self.V_cruise ** 2 * self.MAC * self.c[n] * (self.coefdist[n, 0] - self.coefdist[n + 1, 0]) + self.intload[n, 1] * 0.2 * self.c[n]
            elif n == self.coefdist.shape[0] - 1:
                self.intload[n, 3] = - self.coefdist[n, 3] * 0.5 * self.rho * self.V_cruise ** 2 * self.MAC * self.c[n] * self.coefdist[n, 0] * 2 + self.intload[n, 1] * 0.2 * self.c[n]
            # print(self.intload[n, 1] * 0.2 * self.c[n])
        # print(self.intload)
        return self.intload

    def get_normalstress(self, B):
        # Ixx for 4 booms of area B [mm^2] each
        self.Ixx = 4 * B * (0.07 * self.c * 1000 / 2) ** 2
        # print(self.intload[:, 1], self.c ,self.Ixx)
        self.sigma = 3.8 * self.intload[:, 1] * 1000 * (0.07 * self.c *1000 / 2) / self.Ixx
        return self.sigma, self.sigma_y

    def get_shear_stress(self):
        B = 20
        self.Ixx = 8 * B * (0.07 * self.c * 1000 / 2) ** 2
        self.intload[:, 2] = self.intload[:, 2]
        self.intload[:, 3] = self.intload[:, 3] * 1000
        self.c = self.c * 1000
        # print(self.intload[-1, 2], self.c[-1], self.intload[-1, 3])
        qtop = 3.8 * (self.intload[:, 3]/ (2 * 0.07 * self.c * 0.40 * self.c))
        qleft = 3.8 * (-self.intload[:, 2] / (2 * 0.07 * self.c) + self.intload[:, 3]/ (2 * 0.07 * self.c * 0.40 * self.c))
        qbot = 3.8 * (self.intload[:, 3] / (2 * 0.07 * self.c * 0.40 * self.c))
        qright = 3.8 * (self.intload[:, 2] / (2 * 0.07 * self.c) + self.intload[:, 3] / (2 * 0.07 * self.c * 0.40 * self.c))
        # print(qtop, qleft, qbot, qright)
        print(np.max(np.abs(qtop/5)), np.max(np.abs(qleft/self.tau_str)), np.max(np.abs(qbot/5)), np.max(np.abs(qright/self.tau_str)))
        print(qtop / 5, qleft / self.tau_str, qbot / 5, qright / self.tau_str)
        # print(q1 / self.tau_str, q2 / self.tau_str, q3 / self.tau_str)
        # print(self.intload[:,0])

# dist = load_distribution(df)
# coefdist, c = dist.get_array()
# loaddist = dist.get_loaddist()
# intload = dist.get_intload()
# sigma, sigma_y = dist.get_normalstress(20)
# dist.get_shear_stress()
# print(sigma, sigma_y, '\n end')
# # plot load distribution
# # plt.plot(coefdist[:, 0], coefdist[:, 1])
# # plt.plot(loaddist[:, 0], loaddist[:, 1])
# plt.plot(intload[:, 0], intload[:, 1])
# plt.show()



