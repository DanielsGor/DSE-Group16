import pandas as pd
import numpy as np
# Coordinate system: X Upwards and Z forwards
def boomloaddist(verticalforce, sparpitch, boomlength, n):
    # Define dataframe for storing internal loads
    df = pd.DataFrame(columns=['boomlength', 'Shearint', 'Momentint'])
    df['boomlength'] = np.linspace(0, boomlength, n)
    df = df.set_index('boomlength')

    # Calculating reaction forces
    reacfrontX = verticalforce * (boomlength - sparpitch) / sparpitch
    reacrearX = - verticalforce * boomlength / sparpitch
    for i in range(n):
        if i == 0:
            internalshear = 1
    return None
boomlength = 10
n = 10

df = pd.DataFrame(columns = ['Name', 'Scores', 'Questions'],
                   index = ['a', 'b', 'c'])

df = pd.DataFrame(columns= ['boomlength', 'Shearint', 'Momentint'])
df['boomlength'] = np.linspace(0, boomlength, n)
df = df.set_index('boomlength')
print(df)