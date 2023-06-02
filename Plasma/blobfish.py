import numpy as np
import matplotlib.pyplot as plt
import csv

x = np.asarray([])
y = np.asarray([])
with open('Plasma/blobfish.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        x_dot = float(row['x'])/140
        y_dot = float(row['y'])/140
        x = np.append(x,x_dot)
        y = np.append(y,y_dot)
        print(x_dot,",",y_dot)
        

plt.plot(x,y)
plt.show()