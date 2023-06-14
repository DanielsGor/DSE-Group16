import numpy as np
from constants import df
from get_loaddist import load_distribution

#   Dummy inputs for different span-wise elements
Mx = np.arange(10, 7, -1)
My = np.arange(10, 7, -1)
Ixx = np.arange(10, 8.5, -0.5)
Iyy = np.arange(10, 8.5, -0.5)
Ixy = np.zeros(3)

#   Dummy wing coordinates in nested arrays. Outer list refers to different span-wise elements,
#   whereas inner list corresponds to different points

xwing = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
ywing = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])

def BendingStress(Mx, My, Ixx, Iyy, Ixy, xwing, ywing):
    #   Neutral axis angle from cg coordinate frame
    tana = np.tan(-(My * Ixx - Mx * Ixy) / (Mx * Iyy - My * Ixy))

    #   Initialize arrays
    max_stress = np.zeros(len(My))
    max_stress_loc = np.zeros((2, len(My)))

    for i in range(len(My)):
        #   Find maximum distance from NA for each span increment
        na_dist = np.abs(tana[i] * xwing[i] - ywing[i]) / np.sqrt(tana[i] ** 2 + 1)
        max_dist_i = np.argmax(na_dist)

        #   Stress calculation
        max_stress[i] = ((Mx[i] * Iyy[i] - My[i] * Ixy[i]) * ywing[i][max_dist_i] + (My[i] * Ixx[i] - Mx[i] * Ixy[i]) *
                         xwing[i][max_dist_i]) / (Ixx[i] * Iyy[i] - Ixy[i] ** 2)

        #   Assign maximum stress location values
        max_stress_loc[0][i] = np.array(xwing[i][max_dist_i])
        max_stress_loc[1][i] = np.array(ywing[i][max_dist_i])

    return(max_stress, max_stress_loc)

# max_stress, max_stress_loc = BendingStress(Mx, My, Ixx, Iyy, Ixy, xwing, ywing)
#
# print(max_stress, max_stress_loc)

# Al 2024-T3
sigma_y = 324 # MPa / N/mm^2
tau = 283
G = 28e3 # MPa / N/mm^2
E = 73.1e3 # MPa / N/mm^2
MAC = df['MAC'] # mm
V_cruise = df['V_cruise'] # m/s
rho = df['rho_atm'] # kg/m^3



def get_bendingstress(Mx, B, c):
    Ixx = 4 * B * (0.035 * c) ** 2
    # print(Mx, c, Ixx)
    sigma = (3.8 * Mx * 0.035 * c / Ixx)

    return sigma, sigma_y
# check sign of Vz
def get_shear_stress(Vz, c, Mw):
    # print(Vz, c, Mw)
    qtop = Mw/ (2 * 0.07 * c * 0.40 * c)
    qleft = - Vz / (2 * 0.07 * c) + Mw/ (2 * 0.07 * c * 0.40 * c)
    qbot = Mw / (2 * 0.07 * c * 0.40 * c)
    qright = Vz / (2 * 0.07 * c) + Mw / (2 * 0.07 * c * 0.40 * c)
    # print(qtop, qleft, qbot, qright)
    # print(qtop/tau, qleft/tau, qbot/tau, qright/tau)



dist = load_distribution(df)
coefdist, c = dist.get_array()
loaddist = dist.get_loaddist()
intload = dist.get_intload()
dist.get_shear_stress()

# sigma, sigma_y = get_bendingstress(intload[-1,1]*1000, 20, c[-1]*1000)
# print(sigma, sigma_y)
# print(intload[:, 2], c, intload[:, 3])
get_shear_stress(intload[-1,2], c[-1]*1000, intload[-1,3])
# print(sigma_y)




# b = np.linspace(1495, 0, 41)
# c = np.full(len(b[b>=1490]), 0.8)
# a = np.linspace(0.8, 1.2, len(b[800<b]) - len(b[b>1490]))
# c = np.append(c, a)
# c = np.append(c, np.full(len(b[b<=800]), 1.2))
# print(len(c))


