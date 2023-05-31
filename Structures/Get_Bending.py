import numpy as np

#   Dummy inputs
Mx = np.arange(10, 7, -1) # Dummy bending distribution

My = np.arange(10, 7, -1)

Ixx = np.arange(10, 8.5, -0.5)

Iyy = np.arange(10, 8.5, -0.5)

Ixy = np.zeros(3)

#   Dummy wing coordinates

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
                         xwing[i][max_dist_i]) \
                        / (Ixx[i] * Iyy[i] - Ixy[i] ** 2)

        #   Assign maximum stress location values

        max_stress_loc[0][i] = np.array(xwing[i][max_dist_i])
        max_stress_loc[1][i] = np.array(ywing[i][max_dist_i])

    return(max_stress, max_stress_loc)

max_stress, max_stress_loc = BendingStress(Mx, My, Ixx, Iyy, Ixy, xwing, ywing)

print(max_stress, max_stress_loc)