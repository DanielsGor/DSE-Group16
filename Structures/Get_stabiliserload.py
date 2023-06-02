import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Coordinate system: X Upwards and Z forwards
def boomloaddist(verticalforce, sparpitch, boomlength, n):
    # Define dataframe for storing internal loads
    df = pd.DataFrame(columns=['boomlength', 'shearint', 'momentint'])
    df['boomlength'] = np.linspace(0, boomlength, n)
    df = df.set_index('boomlength')

    # Calculating reaction forces
    reacfrontX = verticalforce * (boomlength - sparpitch) / sparpitch
    reacrearX = - verticalforce * boomlength / sparpitch
    for i in range(n):
        if i * boomlength / n <= sparpitch:
            df.iloc[i, 0] = reacfrontX
        if sparpitch < i * boomlength / n < boomlength:
            df.iloc[i, 0] = reacfrontX + reacrearX
        if i * boomlength / n == boomlength:
            df.iloc[i, 0] = reacfrontX + reacrearX + verticalforce
    for i in range(n):
        if i == 0:
            df.iloc[i, 1] = 0
        else:
            df.iloc[i, 1] = - df.iloc[i, 0] * boomlength / n + df.iloc[i - 1, 1]
        print(df.iloc[i, 1])

    return df

# test boomloaddist function
df = boomloaddist(100, 0.5, 1, 100)

# plot the data of df where the index is the x-axis and the column is the y-axis
plt.plot(df.index, df['shearint'])
plt.plot(df.index, df['momentint'])
plt.show()
