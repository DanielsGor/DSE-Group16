import numpy as np


#   Dummy inputs
Mx = np.arange(10, 0, -1) # Dummy bending distribution

My = np.arange(10, 0, -1)

Ixx = np.arange(10, 5, -0.5)

Iyy = np.arange(10, 5, -0.5)

Ixy = np.zeros(10)

#   Dummy coordinates for the maximum normal stress point

xstress = 1.

ystress = 2.

#   Stress calculation

Sz = ((Mx * Iyy - My * Ixy) * ystress + (My * Ixx - Mx * Ixy) * xstress) / (Ixx * Iyy - Ixy ** 2)

print(Sz)