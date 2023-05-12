import numpy as np
from Variables import initMTOW
# class wheight_estimation
#     def __init__(self):
#         self.weights = {
#             "darmstadt" : np.array([10.5, 3, 3, 0.5, 1, 1, 0.8, 0.2, 1])
#             "concept1" : None
#         }
#
#     def conceptweightestimation(self, initMTOW):
#         self.weights["concept1"] = self.weights["darmstadt"]*initMTOW/sum(self.weights["darmstadt"][1:])

rho = 1.225 #kg/m^3 # m/s
b = 2.2 # m # m^2
AR = 7
S = b**2/AR
c = b/AR # m
MTOW = 6.55*9.81 #kg
Cd0 = 0.03
e = 0.75
k = 1/(np.pi*AR*e)
ROC = 2.8 # m/s
Clmax = 1.3
Vstall = np.sqrt(MTOW/(0.5*Clmax*rho*S))

# Cruise
Clopt = np.sqrt(3*Cd0*np.pi*AR*e)
Cdopt = Cd0 + k*Clopt**2
ClCdopt = Clopt/Cdopt
Vcruise = np.sqrt(MTOW/(0.5*rho*Clopt*S))
Tcruise = (Cd0 + MTOW/(0.5*rho*Vcruise**2*S*np.pi*AR*e))*0.5*rho*Vcruise**2*S

# Take-off
Vtakeoff = 15 # m/s
Ttakeoff = (Cd0 + MTOW/(0.5*rho*Vtakeoff**2*S*np.pi*AR*e))*0.5*rho*Vtakeoff**2*S+MTOW*ROC/Vtakeoff

# Glide
Clglide = np.sqrt(Cd0*np.pi*AR*e)
Cdglide = Cd0 + k*Clglide**2
ClCdglide = Clglide/Cdglide
Vglide = np.sqrt(MTOW/(0.5*rho*Clglide*S))

# ClCd = 7.6
# Cl = np.arange(0,2,0.01)
# ClCd = Cl/(Cd0 + Cl**2/(np.pi*AR*e))
# Clcruise = Cl[np.argmax(ClCd)]
# alphacruise = Clcruise/(2*np.pi)
Vcruise = np.sqrt(MTOW/(0.5*rho*Clopt*S))


# for i in Cl:
#     Cd = Cd0 + i**2/(0.5*AR*e)
#     CdCl = Cd/i
#     np.arange(CdClarray, CdCl)





q=1
# Weigth -> lift -> drag