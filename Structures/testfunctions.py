import numpy as np
from Get_Shape import spar_w, spar_t, x_spars, y_spars, skin_t, totalcg_x, totalcg_y
print('begin test')


def IdealisedBoomtest(w_cap, t_cap, x_cgcap, y_cgcap, t_skin, cg_airfoil, Mx, My, spline, it):
    cg_cap = np.array([x_cgcap, y_cgcap])
    for i in range(len(cg_cap[0])):
        cg_cap[:,i] = cg_cap[:,i] - cg_airfoil
    sigma = np.zeros(len(cg_cap[0]))
    B = np.full(4, w_cap * t_cap)
    print(B)
    Bskin = np.zeros(4)
    Btot = np.zeros((it,4))
    for i in range(it):
        Ixx = np.sum(cg_cap[1,:] ** 2 * (B + Bskin))
        Iyy = np.sum(cg_cap[0,:] ** 2 * (B + Bskin))
        Ixy = np.sum(cg_cap[0,:] * cg_cap[1,:] * (B + Bskin))
        print(Ixy)
        for j in range(len(cg_cap[0])):
            # Calculates sigma in whatever Mx and My are given in divided by mm^2
            sigma[j] = ((Mx * Iyy - My * Ixy) / (Ixx * Iyy - Ixy ** 2)) * cg_cap[1, j] + ((My * Ixx - Mx * Ixy) / (Ixx * Iyy - Ixy ** 2)) * cg_cap[0, j]
        Bskin[0] = t_cap * (np.abs(cg_cap[1,0] - cg_cap[1,1])) / 6 * (2 + sigma[1]/sigma[0]) + t_skin * (spline[1]) / 6 * (2 + sigma[2]/sigma[0])
        Bskin[1] = t_cap * (np.abs(cg_cap[1,1] - cg_cap[1,0])) / 6 * (2 + sigma[0]/sigma[1]) + t_skin * (spline[3]) / 6 * (2 + sigma[3]/sigma[1])
        Bskin[2] = t_cap * (np.abs(cg_cap[1,2] - cg_cap[1,3])) / 6 * (2 + sigma[3]/sigma[2]) + t_skin * (spline[1]) / 6 * (2 + sigma[0]/sigma[1])
        Bskin[3] = t_cap * (np.abs(cg_cap[1,3] - cg_cap[1,2])) / 6 * (2 + sigma[2]/sigma[3]) + t_skin * (spline[3]) / 6 * (2 + sigma[1]/sigma[3])
        Btot[i,:] = B + Bskin
    print(Btot)
    return Btot

# test = IdealisedBoomtest(spar_w, spar_t, x_spars, y_spars, skin_t, np.array([totalcg_x, totalcg_y]), 100, 100, np.array([700, 700, 700, 700]), 10)
# print('end test')

class ClassA(object):
    def __init__(self):
        self.var1 = 1
        self.var2 = 2

    def methodA(self):
        self.var1 = self.var1 + self.var2
        return self.var1

class ClassB(ClassA):
    def __init__(self, class_a):
        self.var1 = class_a.var1
        self.var2 = class_a.var2

object1 = ClassA()
sum = object1.methodA()
object2 = ClassB(object1)
print(sum)