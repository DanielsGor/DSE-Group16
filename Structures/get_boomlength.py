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

def material_properties(mat):
    rho = None
    E_modulus_tensile = None
    sigma_y_tensile = None
    sigma_y_compressive = None
    if mat == 'balsa':
        rho = 104
        E_modulus_tensile = 2.239*10**9
        sigma_y_tensile =  7.501*10*6
        sigma_y_compressive = 6.523*10**6
    elif mat == 'aluminum 2024-T3':
        rho = 2780
        E_modulus_tensile = 73.1*10**9
        sigma_y_tensile = 275*10**6
        sigma_y_compressive = 275*10**6
    return(rho, E_modulus_tensile, sigma_y_tensile, sigma_y_compressive)

def get_Lh_Sh(L, xdif):
    lh = xdif+L
    Lh = 10.93/(2 * lh)
    Sh = .98/lh
    return(Lh, Sh)

def emp_weight(Sh, t_skin, rho):
    Wemp = 8*Sh*t_skin*rho
    return(Wemp)

def finalmass(length, xdif, tskin, rho_tail,thicknessV, thicknessH, rho_boom, width, height, E_modulus_boom, type):
    Lh, Sh = get_Lh_Sh(length, xdif)
    Mempennage = emp_weight(Sh, tskin, rho_tail)
    Mboom, Ixx, Iyy = boom_properties(type, thicknessV, thicknessH, rho_boom, length, width, height)
    M = 2 * Mboom + Mempennage
    F = Lh - (Mempennage * 9.81) / 2
    deflection = deflection_angle_by_pointforce(F, length, E_modulus_boom, Ixx, Mboom)
    My = F * length
    maximum_stress = BendingStress(0, My, Ixx, Iyy, type, width, height)[0]
    return(M, maximum_stress, deflection)


lengthrange = np.arange(1, 2, .1)
tskinrange = np.arange(.0005, .001, .0001)
thicknessVrange = np.arange(.0005, .001, .0001)
thicknessHrange = np.arange(.0005, .001, .0001)
widthrange = np.arange(.01, .10, .01)
heightrange = np.arange(.01, .10, .01)
typ = ['rectangular', 'circular']

optimal_config = {'length': None, 'skin thickness': None, 'vertical boom thickness': None,
                  'horizontal boom thickness': None, 'width': None, 'height': None,
                  'type': None, 'material': None, 'mass': float('inf')}

for i in lengthrange:
    for j in tskinrange:
        for k in thicknessVrange:
            for l in thicknessHrange:
                for m in widthrange:
                    for n in heightrange:
                        for o in typ:
                            for p in ['aluminum 2024-T3']:
                                r, E, st, sc = material_properties(p)
                                M, s, d = finalmass(i, .0222, j, 104, k, l, r, m, n, E, o)
                                if M < optimal_config['mass'] and s < sc and d < 0.5:
                                    optimal_config['length'] = i
                                    optimal_config['skin thickness'] = j
                                    optimal_config['vertical boom thickness'] = k
                                    optimal_config['horizontal boom thickness'] = l
                                    optimal_config['width'] = m
                                    optimal_config['height'] = n
                                    optimal_config['type'] = o
                                    optimal_config['mass'] = M
                                    optimal_config['stress'] = s
                                    optimal_config['deflection'] = d
                                    optimal_config['material'] = p
                                    print(optimal_config)
                                    print('------------------------------------')

                                else:
                                    continue

