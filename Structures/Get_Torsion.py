import numpy as np
from Get_Shape import *
from constants import df
# torsion = np.arange(10, 0, -1)
# J = np.arange(10, 5, -.5)
#
# #Thin-walled closed sections
# t = .02                     #Define wall thickness
# Am = np.arange(10, 5, -.5)  #Define enclosed area along span
# tau = torsion/(2*t*Am)
# print(tau)

class multicell:
    def __init__(self):
        self.cg = get_cg(x_spars, y_spars, spar_w, spar_t)
        self.momentArm = df['l_boom'] - self.cg[0]
        self.A = np.ones(3)
        self.q = np.ones(3)
        self.bigMAT = np.zeros((4,4))
        self.G  = 28e9
        self.s = np.ones(7)
        self.t = np.ones(2)
    def getTorsion(self, horstabload):
        Mz = horstabload*self.momentArm

        Tlist = 2 * self.A
        for i in range(len(Tlist)):
            self.bigMAT[3,i] = Tlist[i]
            self.bigMAT[i,3] = -1
        self.bigMAT[0,0] = 0.5*self.s[0]/(self.A[0]*self.G*self.t[0]) + \
                           0.5*self.s[5]/(self.A[0]*self.G*self.t[1])
        self.bigMAT[0,1] = -0.5*self.s[5]/(self.A[0]*self.G*self.t[1])
        self.bigMAT[1,0] = -0.5*self.s[5]/(self.A[1]*self.G*self.t[1])
        self.bigMAT[1,1] = 0.5*self.s[1]/(self.A[1]*self.G*self.t[0]) + \
                           0.5*self.s[4]/(self.A[1]*self.G*self.t[0]) + \
                           0.5*self.s[5]/(self.A[1]*self.G*self.t[1]) + \
                           0.5*self.s[6]/(self.A[1]*self.G*self.t[1])
        self.bigMAT[1,2] = -0.5*self.s[6]/(self.A[1]*self.G*self.t[1])
        self.bigMAT[2,1] = -0.5*self.s[6]/(self.A[2]*self.G*self.t[1])
        self.bigMAT[2,2] = 0.5*self.s[2]/(self.A[2]*self.G*self.t[0]) + \
                           0.5*self.s[6]/(self.A[2]*self.G*self.t[1]) + \
                           0.5*self.s[3]/(self.A[2]*self.G*self.t[0])
        righthandside = np.array([0, 0, 0, Mz])
        solved = np.linalg.solve(self.bigMAT, righthandside)

        return solved

mc = multicell()
print('money \n', mc.getTorsion(1000))