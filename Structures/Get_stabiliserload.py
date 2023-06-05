import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from constants import df
# Coordinate system: X Upwards and Z forwards

class boomShit:
    def __init__(self):
        self.l_boom = df['l_boom']
        self.d_boom = df['d_boom']
        self.b_boom = df['b_boom']
        self.G = [df['G_A950']]
        self.J_boomSide = None
        self.J_frontSpar = None
        self.J_rearSpar = None
        self.torsConstFront = None
        self.torsConstRear = None
        self.w_frontCap = df['w_frontCap']
        self.w_rearCap = df['w_rearCap']
        self.w_frontWeb = df['w_frontWeb']
        self.w_rearWeb = df['w_rearWeb']
        self.t_frontCap = df['t_frontCap']
        self.t_rearCap = df['t_rearCap']
        self.t_frontWeb = df['t_frontWeb']
        self.t_rearWeb = df['t_rearWeb']


    def boomDefl(self):
        self.J_boomSide = sp.integrate.dblquad(lambda x, y: x ** 2 + y ** 2, -self.d_boom / 2, self.d_boom / 2,
                                               -self.l_boom / 2, self.l_boom / 2)
        self.J_frontSpar = sp.integrate.dblquad(lambda x, y: x ** 2 + y ** 2, self.w_frontWeb / 2, self.w_frontWeb / 2 + self.t_frontCap,
                                                -self.w_frontCap / 2, self.w_frontCap / 2) * 2
        + sp.integrate.dblquad(lambda x, y: x ** 2 + y ** 2, - self.w_frontWeb / 2, self.w_frontWeb / 2, - self.t_frontWeb / 2, self.t_frontWeb / 2,)
        self.J_rearSpar = sp.integrate.dblquad(lambda x, y: x ** 2 + y ** 2, self.w_rearWeb / 2, self.w_rearWeb / 2 + self.t_rearCap,
                                               -self.w_rearCap / 2, self.w_rearCap / 2) * 2
        + sp.integrate.dblquad(lambda x, y: x ** 2 + y ** 2, - self.w_rearWeb / 2, self.w_rearWeb / 2, - self.t_rearWeb / 2, self.t_rearWeb / 2,)
        self.torsConstFront = self.G[0] * self.J_frontSpar[0] / self.l_boom
        self.torsConstRear = self.G[0] * self.J_rearSpar[0] / self.l_boom



def boomLoadDist(verticalforce, sparpitch, boomlength, n):
    # Define dataframe for storing internal loads
    df = pd.DataFrame(columns=['boomlength', 'shearint', 'momentint'])
    df['boomlength'] = np.linspace(0, boomlength, n)
    df = df.set_index('boomlength')

    # Calculating reaction forces
    reacfrontX = verticalforce * (boomlength - sparpitch) / sparpitch
    reacrearX = - verticalforce * boomlength / sparpitch
    for i in range(n):
        if i * boomlength / n <= sparpitch:
            df.iloc[i, 0] = reacfrontX
        if sparpitch < i * boomlength / n < boomlength:
            df.iloc[i, 0] = reacfrontX + reacrearX
        if i * boomlength / n == boomlength:
            df.iloc[i, 0] = reacfrontX + reacrearX + verticalforce
    for i in range(n):
        if i == 0:
            df.iloc[i, 1] = 0
        else:
            df.iloc[i, 1] = - df.iloc[i, 0] * boomlength / n + df.iloc[i - 1, 1]
        print(df.iloc[i, 1])

    return df


class fuselage:
    def __init__(self):
        # create self attributes with the lines of code below
        self.length = df['fus_l']  # Length of the fuselage in meters
        self.width = df['fus_w']  # Width of the fuselage in meters
        self.height = df['fus_h']  # Height of the fuselage in meters
        self.skin_thickness = df['t_skin']  # Thickness of the fuselage skin in meters
        self.stringer_pitch = df['str_pitch']  # Spacing between stringers in meters
        self.stringer_width = df['str_w']  # Width of the stringers in meters
        self.stringer_height = df['str_h']  # Height of the stringers in meters
        self.stringer_thickness = df['str_t']  # Thickness of the stringers in meters
        self.balsa_tens = df['balsa_tens']  # Tensile strength of balsasud ultralite in MPa
        self.balsa_comp = df['balsa_comp']  # Compressive strength of balsasud ultralite in MPa
        self.internal_shear = None
        self.internal_bending = None
        self.pitch_list = None
        self.normal_stress = None
        self.p = None
    def test(self):
        print(self.length)
