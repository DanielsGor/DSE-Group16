import numpy as np
import math

#   Calculate maximum bending stress for different dimensions
#   Assume Ixy for tail booms is 0
def BendingStress(Mx, My, Ixx, Iyy, type, width, height):
    #   Neutral axis angle from cg coordinate frame
    tana = np.tan(-(My * Ixx) / (Mx * Iyy))
    x = np.arange(0)
    y = np.arange(0)
    if type == 'circular':
        x = np.append(x, width * np.cos(np.arctan(tana) + np.pi / 2))
        x = np.append(x, width * np.cos(np.arctan(tana) - np.pi / 2))
        y = np.append(y, width * np.sin(np.arctan(tana) + np.pi / 2))
        y = np.append(y, width * np.sin(np.arctan(tana) - np.pi / 2))
    elif type == 'rectangular':
        x = np.append(x, width / 2)
        x = np.append(x, width / 2)
        x = np.append(x, -width / 2)
        x = np.append(x, -width / 2)
        y = np.append(y, height / 2)
        y = np.append(y, -height / 2)
        y = np.append(y, height / 2)
        y = np.append(y, -height / 2)


    stress = np.zeros(len(x))
    for i in range(len(x)):
        stress[i] = ((Mx * Iyy) * y[i] + (My * Ixx) * x[i]) / (Ixx * Iyy)

    max_stress = np.amax(stress)
    max_stress_loc = np.array([x[np.argmax(stress)], y[np.argmax(stress)]])

    return(max_stress, max_stress_loc)



def inertia_thin_walled_circular_section(thickness, diameter)
    Ix = (np.pi * thickness * diameter ** 2) / 8
    J = (np.pi * thickness * diameter ** 2) / 4
    return(Ix, J)

def boom_properties(type, thicknessV, thicknessH, rho, length, width, height):
    Ixx = None
    Iyy = None
    mass = None
    if type == 'circular':
        mass = np.pi*width*thicknessV*rho*length
        Ixx = (np.pi * thicknessV * width ** 2) / 8
        Iyy = Ixx
    elif type == 'rectangular':
        mass = (2*width*thicknessH+2*height*thicknessV)*length*rho
        Ixx = 2 * ((height*thicknessV**3)/12 + width*thicknessV*(height/2)**2)
        Iyy = 2 * ((width*thicknessH**3)/12 + height*thicknessH*(width/2)**2)
    return(mass, Ixx, Iyy)


def deflection_angle_by_pointforce(force, length, E_modulus, Ix, Mboom):
    deflection = ((force*length**2)/(2*E_modulus*Ix)+(Mboom/length*length**3)/(6*E_modulus*Ix))*180/np.pi
    return(deflection)

def get_Lh_Sh(L, xdif):
    lh = xdif+L
    Lh = 10.93/lh
    Sh = .98575/lh
    return(Lh, Sh)

def emp_weight(Sh, t_skin, rho):
    Wemp = 8*Sh*t_skin*rho
    return(Wemp)

def finalmass(length, xdif, tskin, rho_tail,thicknessV, thicknessH, rho_boom, width, height, E_modulus_boom):
    Lh, Sh = get_Lh_Sh(length, xdif)
    Mempennage = emp_weight(Sh, tskin, rho_tail)
    Mboom, Ixx, Iyy = boom_properties(type, thicknessV, thicknessH, rho_boom, length, width, height)
    M = Mboom + Mempennage
    deflection = deflection_angle_by_pointforce(force, length, E_modulus_boom, Ix, Mboom)
    maximum_stress =
    print(deflection)
    print(maximum_stress)
    return(finalmass)

finalmass = finalmass(1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
print(finalmass)