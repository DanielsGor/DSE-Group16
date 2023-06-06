import numpy as np
torsion = np.arange(10, 0, -1)
J = np.arange(10, 5, -.5)

#Thin-walled closed sections
t = .02                     #Define wall thickness
Am = np.arange(10, 5, -.5)  #Define enclosed area along span
tau = torsion/(2*t*Am)
print(tau)