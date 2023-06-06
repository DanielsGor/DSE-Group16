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
        self.G = df['G_A950']
        self.J_boomSide = None
        self.J_frontSpar = None
        self.J_rearSpar = None
        self.Kappa_f = None
        self.Kappa_r = None
        self.k_f = None
        self.k_r = None
        self.w_frontCap = df['w_frontCap']
        self.w_rearCap = df['w_rearCap']
        self.w_frontWeb = df['w_frontWeb']
        self.w_rearWeb = df['w_rearWeb']
        self.t_frontCap = df['t_frontCap']
        self.t_rearCap = df['t_rearCap']
        self.t_frontWeb = df['t_frontWeb']
        self.t_rearWeb = df['t_rearWeb']
        self.p_spars = df['p_spars']
        self.Mmat = None
        self.Kmat = None
        self.m_boom = self.d_boom ** 2 * np.pi / 4 * self.l_boom * df['rho_A950']
        self.I_boomCross = None
        self.E = df['E_A950']
        self.Ixxf = 500
        self.Ixxr = 500
        self.x = np.array([None, None])
        self.F = 100
        self.initCond = [0, 0, 0, 0]
        self.jac = None


    def boomDefl(self):
        self.J_boomSide = sp.integrate.dblquad(lambda x, y: x ** 2 + y ** 2, -self.d_boom / 2, self.d_boom / 2,
                                               -self.l_boom / 2, self.l_boom / 2)[0]
        self.J_frontSpar = sp.integrate.dblquad(lambda x, y: x ** 2 + y ** 2, self.w_frontWeb / 2, self.w_frontWeb / 2 + self.t_frontCap,
                                                -self.w_frontCap / 2, self.w_frontCap / 2)[0] * 2 \
                           + sp.integrate.dblquad(lambda x, y: x ** 2 + y ** 2, -self.w_frontWeb / 2, self.w_frontWeb / 2,
                                                  -self.t_frontWeb / 2, self.t_frontWeb / 2)[0]
        self.J_rearSpar = sp.integrate.dblquad(lambda x, y: x ** 2 + y ** 2, self.w_rearWeb / 2, self.w_rearWeb / 2 + self.t_rearCap,
                                               -self.w_rearCap / 2, self.w_rearCap / 2)[0] * 2\
                           + sp.integrate.dblquad(lambda x, y: x ** 2 + y ** 2, -self.w_rearWeb / 2, self.w_rearWeb / 2,
                                                  -self.t_rearWeb / 2, self.t_rearWeb / 2)[0]
        self.I_boomCross = np.pi * self.d_boom ** 4 / 64
        self.Kappa_f = self.G * self.J_frontSpar / self.l_boom
        self.Kappa_r = self.G * self.J_rearSpar / self.l_boom
        self.k_f = 3 * self.E * self.Ixxf / self.b_boom ** 3
        self.k_r = 3 * self.E * self.Ixxr / self.b_boom ** 3
        self.Mmat = np.array([[self.m_boom, 0],[0, self.J_boomSide]])
        self.Kmat = np.array([[self.k_f + self.k_r, -(self.k_f + self. k_r)*self.l_boom/2 + self.k_r*self.p_spars],
                              [-self.k_f * self.l_boom / 2 -self.k_r * (self.l_boom / 2 + self.p_spars),
                               self.Kappa_f + self.Kappa_r + self.k_f * (self.l_boom / 2) ** 2 + self.k_r
                               * (self.l_boom / 2 - self.p_spars) ** 2]])
        self.F = np.array([self.F, self.F * self.l_boom / 2])
        # x, y, theta, phi = self.initCond
        # t = np.linspace(0, 5, 100)
        # f = [y,
        #      (-self.k_f*(x-theta*self.l_boom/2) - self.k_r*(x-theta*(self.l_boom/2-self.p_spars)) + self.F)/self.m_boom,
        #      phi,
        #      ((-self.Kappa_f - self.Kappa_r - (self.l_boom/2)**2*self.k_f - (self.l_boom/2-self.p_spars)**2*self.k_r)*theta
        #      + (self.k_f*self.l_boom/2 + self.k_r*(self.l_boom/2-self.p_spars))*x + self.F*self.l_boom/2)/self.J_boomSide]
        # self.jac = [[0, 1, 0, 0],
        #        [(-self.k_f * self.l_boom / 2 - self.k_r * (self.l_boom / 2 - self.p_spars)) / self.m_boom, 0,
        #         (-self.k_f * (x - self.l_boom / 2) - self.k_r * (x - self.l_boom / 2 + self.p_spars)) / self.m_boom, 0],
        #        [0, 0, 0, 1],
        #        [(self.k_f * self.l_boom / 2 + self.k_r * (self.l_boom / 2 - self.p_spars)) / self.J_boomSide, 0,
        #         ((-self.Kappa_f - self.Kappa_r - 2 * (self.l_boom / 2) * self.k_f - 2 * (
        #                     self.l_boom / 2 - self.p_spars) * self.k_r) * theta
        #          + (self.k_f * self.l_boom / 2 + self.k_r * (
        #                             self.l_boom / 2 - self.p_spars)) * x + self.F * self.l_boom / 2) / self.J_boomSide,
        #         0]]
        # sol = sp.integrate.odeint(f, self.initCond, t, Dfun=self.jac, atol=abserr, rtol=relerr)

        return None

    def defineode(self, y, t):
        x, v, theta, omega = y
        f = [v,
             (-self.k_f * (x - theta * self.l_boom / 2) - self.k_r * (
                         x - theta * (self.l_boom / 2 - self.p_spars)) + self.F) / self.m_boom,
             omega,
             ((-self.Kappa_f - self.Kappa_r - (self.l_boom / 2) ** 2 * self.k_f - (
                         self.l_boom / 2 - self.p_spars) ** 2 * self.k_r) * theta
              + (self.k_f * self.l_boom / 2 + self.k_r * (
                                 self.l_boom / 2 - self.p_spars)) * x + self.F * self.l_boom / 2) / self.J_boomSide]
        return f

    def solveode(self):
        y0 = self.initCond
        t = np.linspace(0, 10, 101)
        abserr = 1.0e-8
        relerr = 1.0e-6
        sol = sp.integrate.odeint(self.defineode, y0, t, atol=abserr, rtol=relerr)
        return sol

bs = boomShit()
bs.boomDefl()
sol = bs.solveode()
print(sol)

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
