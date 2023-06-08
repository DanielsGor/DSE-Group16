import numpy as np
import math



#   Calculate maximum bending stress for different dimensions
def BendingStress(Mx, My, Ixx, Iyy, Ixy, xboom, yboom):
    #   Neutral axis angle from cg coordinate frame
    tana = np.tan(-(My * Ixx - Mx * Ixy) / (Mx * Iyy - My * Ixy))

    #   Find maximum distance from NA for each span increment
    na_dist = np.abs(tana * xboom - yboom) / np.sqrt(tana ** 2 + 1)
    max_dist_i = np.argmax(na_dist)

    #   Stress calculation
    max_stress = ((Mx * Iyy - My * Ixy) * yboom[max_dist_i] + (My * Ixx - Mx * Ixy) *
                     xboom[max_dist_i]) / (Ixx * Iyy - Ixy ** 2)

    #   Assign maximum stress location values
    max_stress_loc = [np.array(xboom[max_dist_i]), np.array(yboom[max_dist_i])]

    return(max_stress, max_stress_loc)



def inertia_thin_walled_circular_section(thickness, diameter)
    Ix = (np.pi * thickness * diameter ** 2) / 8
    J = (np.pi * thickness * diameter ** 2) / 4
    return(Ix, J)
def get_mass(thickness, diameter, rho, length):
    mass = np.pi*diameter*thickness*rho*length
    return(mass)
def deflection_angle_by_pointforce(force, length, E_modulus, Ix):
    d
