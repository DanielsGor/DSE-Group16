import numpy as np
import glob
import pandas as pd

# Get CSV files list from a folder
dfL = pd.read_csv(r"C:\Users\oprsc\PycharmProjects\DSE-Group16\Structures\CSV\L-MH115-30May.csv")
dfD = pd.read_csv(r"C:\Users\oprsc\PycharmProjects\DSE-Group16\Structures\CSV\D-MH115-30May.csv")
dfCM = pd.read_csv(r"C:\Users\oprsc\PycharmProjects\DSE-Group16\Structures\CSV\CM-MH115-30May.csv")
dfBM = pd.read_csv(r"C:\Users\oprsc\PycharmProjects\DSE-Group16\Structures\CSV\BM-MH115-30May.csv")

# remove last column of each dataframe
dfL = dfL.iloc[:, :-2]

# Combine all load cases into one dataframe and use span as index
df = pd.concat([dfL, dfD['load'], dfCM['load'], dfBM['load']], axis=1)
df = df.set_index('span')

# Change column names to load case names
df.columns = ['L', 'D', 'CM', 'BM']

print(df)
print(np.trapz(df['L'], df.index))

# Half the dataframe
df = df[df.index > 0]

# reverse rows of dataframe
df = df.iloc[::-1]



# test = np.zeros(df.shape[0])
# verBM = np.zeros(df.shape[0])
#
# for i in range(df.shape[0]):
#     if i > 0:
#         for e in range(i+1):
#             test[e] = (df.index[i - e] - df.index[i]) * np.sqrt(df.iloc[i - e, 0] ** 2 + df.iloc[i - e, 1] ** 2)
#     verBM[i] = sum(test)

