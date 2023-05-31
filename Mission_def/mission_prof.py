import sys
print(sys.path)
import numpy as np
import matplotlib.pyplot as plt
# Measurement area:
d = 50      #m
L = 1200    #m
w = 600     #m

# Glide/climb ratio
GC = np.arange(0,50,10001)

#Boustrophedon
R_b = w*L/d + w/GC * (L/d-1)

#Zamboni
r_big = 1/4*L
r_small = r_big - 1/2*d
R_z = w*L/d + (L/(2*d)-1)*np.pi*r_small +  L/(2*d)*np.pi*r_big

plt.plot(GC, R_b)
plt.vlines(r_small/w,0,30000)
plt.axhline(R_z)
plt.show()
print("fuck")