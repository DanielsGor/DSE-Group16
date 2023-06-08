import numpy as np
import math
def inertia_thin_walled_circular_section(thickness, diameter)
    Ix = (np.pi * thickness * diameter ** 2) / 8
    J = (np.pi * thickness * diameter ** 2) / 4
    return(Ix, J)
def get_mass(thickness, diameter, rho, length):
    mass = np.pi*diameter*thickness*rho*length
    return(mass)
def deflection_angle_by_pointforce(force, length, E_modulus, Ix):
    d

def get_Lh_Sh(L, xdif):
    lh = xdif+L
    Lh = 10.93/lh
    Sh = .98575/lh
    return(Lh, Sh)

def boom_weight(Sh, t_skin, rho):
    Wemp = 8*Sh*t_skin*rho
    return(Wemp)


