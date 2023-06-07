import numpy as np
import glob
import pandas as pd
from constants import df

class load_distribution:
    def __init__(self):
        self.V_cruise = df['V_cruise']  # [m/s] cruise speed
        self.rho = df['rho_atm']  # [kg/m^3] air density
        self.MAC = df['MAC']  # [m] chord
        self.dfL = pd.read_csv(r"C:\Users\oprsc\PycharmProjects\DSE-Group16\Structures\CSV\lift_dist7May.csv")
        self.coefdist = None
        self.loaddist = None

    def get_array(self):
        self.dfL = dfL.iloc[:, 0:2]
        self.fdfL.columns = ['span', 'cl']

        # Half the dataframe
        self.dfL = dfL[dfL.iloc[:, 0] > 0]

        # reverse rows of dataframe
        self.dfL = dfL.iloc[::-1]

        # Turn dataframe into array and divide by 1000 to get meters
        self.coefdist = np.array(dfL)
        self.coefdist[:, 0] = self.coefdist[:, 0] / 1000
        # create load distribution array
        self.coefdist = np.zeros((self.coefdist.shape[0], 2))
        self.coefdist[:, 0] = self.coefdist[:, 0]

    def get_loaddist(self, loadcase):
        for i in range(self.coefdist.shape[0]):
            if i == 0:
                self.loaddist[i, 1] = 0.5 * self.coefdist[i, 1] * V_cruise ** 2 * rho * MAC * (
                            self.loaddist[i, 0] - self.loaddist[i + 1, 0])
            if 1 <= i <= self.loadcoef.shape[0] - 2:
                self.loaddist[i, 1] = 0.5 * self.coefdist[i, 1] * V_cruise ** 2 * rho * MAC * (
                            (self.loaddist[i, 0] + self.loaddist[i - 1, 0]) / 2 - (self.loaddist[i, 0] + self.loaddist[i + 1, 0]) / 2)
            if i == self.loadcoef.shape[0] - 1:
                self.loaddist[i, 1] = 0.5 * self.coefdist[i, 1] * V_cruise ** 2 * rho * MAC * (self.loaddist[i - 1, 0] - self.loaddist[i, 0])


# define atmospheric conditions
V_cruise = df['V_cruise']  # [m/s] cruise speed
rho = df['rho_atm']  # [kg/m^3] air density
MAC = 0.336789 # [m] chord

# Get CSV files list from a folder and add to dataframe with span as index
dfL = pd.read_csv(r"C:\Users\oprsc\PycharmProjects\DSE-Group16\Structures\CSV\lift_dist7May.csv")
# dfD = pd.read_csv(r"C:\Users\oprsc\PycharmProjects\DSE-Group16\Structures\CSV\drag_distribution6May.csv")
# dfc = pd.read_csv(r"C:\Users\oprsc\PycharmProjects\DSE-Group16\Structures\CSV\chord_distribution6May.csv")

dfL = dfL.iloc[:, 0:2]
dfL.columns = ['span', 'cl']
print(dfL['span'][0])
# dfL.set_index('span', inplace=True)
# dfloads = pd.concat([dfL, dfD['cd'], dfc['chord']], axis=1)

# Half the dataframe
dfL = dfL[dfL.iloc[:,0] > 0]

# reverse rows of dataframe
dfL = dfL.iloc[::-1]

loadcoef = np.array(dfL)
loadcoef[:, 0] = loadcoef[:, 0] / 1000
V_cruise = df['V_cruise']
loaddist = np.zeros((loadcoef.shape[0], 2))
loaddist[:, 0] = loadcoef[:, 0]
lst = []
for i in range(loadcoef.shape[0]):
    if i == 0:
        loaddist[i, 1] = 0.5 * loadcoef[i, 1] * V_cruise ** 2 * rho * MAC * (loaddist[i, 0] - loaddist[i + 1, 0])
        lst.append((loaddist[i, 0] - loaddist[i + 1, 0]))
    if 1 <= i <= loadcoef.shape[0]-2:
        loaddist[i, 1] = 0.5 * loadcoef[i, 1] * V_cruise ** 2 * rho * MAC * ((loaddist[i, 0] + loaddist[i - 1, 0]) / 2 - (loaddist[i, 0] + loaddist[i + 1, 0]) / 2)
        lst.append(((loaddist[i, 0] + loaddist[i - 1, 0])/2 - (loaddist[i, 0]+loaddist[i + 1, 0])/2))
    if i == loadcoef.shape[0]-1:
        loaddist[i, 1] = 0.5 * loadcoef[i, 1] * V_cruise ** 2 * rho * MAC * (loaddist[i - 1, 0] - loaddist[i, 0])
        lst.append((loaddist[i, 0] - loaddist[i - 1, 0]))

# Plot load distribution and load coefficient distribution
import matplotlib.pyplot as plt
plt.plot(loaddist[:, 0], loaddist[:, 1])
# plt.plot(loadcoef[:, 0], loadcoef[:, 1])
plt.show()




# 0.5 cl rho V^2 S

# # remove last column of each dataframe
# dfL = dfL.iloc[:, :-2]
#
# # Combine all load cases into one dataframe and use span as index
# df = pd.concat([dfL, dfD['load'], dfCM['load'], dfBM['load']], axis=1)
# df = df.set_index('span')
#
# # Change column names to load case names
# df.columns = ['L', 'D', 'CM', 'BM']
#
# # print(np.trapz(df['L'], df.index))
#
# # Half the dataframe
# df = df[df.index > 0]
#
# # reverse rows of dataframe
# df = df.iloc[::-1]
#
#
#
# # test = np.zeros(df.shape[0])
# # verBM = np.zeros(df.shape[0])
# #
# # for i in range(df.shape[0]):
# #     if i > 0:
# #         for e in range(i+1):
# #             test[e] = (df.index[i - e] - df.index[i]) * np.sqrt(df.iloc[i - e, 0] ** 2 + df.iloc[i - e, 1] ** 2)
# #     verBM[i] = sum(test)
#
