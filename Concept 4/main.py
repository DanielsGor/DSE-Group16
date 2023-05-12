#airfoil = 'NACA4412'

#Environment
rho = 1.225 #kg/m^3
g = 9.81 #m/s^2


MTOM = 6.55 * 1.3 #kg
MTOW = MTOM * 9.81 #N

#Velocity
V_launch = 15 #m/s
V_stall = V_launch / 1.4 #m/s
V_climb = 15 #m/s
V_cruise = 15 #m/s

#Wing parameters
b = 0.822 * MTOM**0.572 #m #Paper by Verstraete
S = 0.192 * MTOM**0.737 #m^2 #Paper by Verstraete
AR = b**2 / S # -
sweep = 0 #deg #Raymer book
taper = 0.5 # - #Raymer book
dihedral = 3 #deg #Raymer book

AR_canard = 8 # - #Raymer book
sweep_canard = 0 #deg #Raymer book
taper_canard = 0.5 # - #Raymer book
dihedral_canard = 0 #deg #Raymer book

AR_vtail = 1.5 # - #Raymer book
sweep_vtail = 20 #deg #Raymer book
taper_vtail = 0.6 # - #Raymer book

#Wing loading, Power loading
Wing_loading = MTOW / S #N/m^2

#Aerodynamic parameters - DATCOM
C_Lmax = Wing_loading / (0.5 * rho * V_stall**2) # - 




#print all wing parameters
print('Wing parameters:')
print('b = ', b, 'm')
print('S = ', S, 'm^2')
print('AR = ', AR)
print('sweep = ', sweep, 'deg')
print('taper = ', taper)
print('dihedral = ', dihedral, 'deg')
print('AR_canard = ', AR_canard)
print('sweep_canard = ', sweep_canard, 'deg')
print('taper_canard = ', taper_canard)
print('dihedral_canard = ', dihedral_canard, 'deg')
print('AR_vtail = ', AR_vtail)
print('sweep_vtail = ', sweep_vtail, 'deg')
print('taper_vtail = ', taper_vtail)
print((2*S)/(b*(1+taper)), taper * (2*S)/(b*(1+taper)))