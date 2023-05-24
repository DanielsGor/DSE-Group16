import pandas as pd
import numpy as np

### CONSTANTS ###
#linear model relating mass and power of propulsion system (from Louis)
m1, p1 = 2.7, 10
m2, p2= 70, 200
dmdp = (m2-m1)/(p2-p1)

#program constants
convergence = 0.0005
read_file = "Preliminary Design\Preliminary design.xlsx"
read_sheet = "Class_1_Newer"

#print output values
PRINT = False
print_file = "Preliminary Design\Preliminary iteration.xlsx"
print_sheet = "Iteration_results"

### FUNCTIONS ###
# xlsx file processing
def read_xlsx_input_data(file = read_file):
    file = pd.ExcelFile(file)
    dat = pd.read_excel(file,header = None, sheet_name = read_sheet).to_numpy() [1:16,1]
    return dat

def new_iteration (array):
    new_array = np.array(dict.items())
    array_new = np.concatenate((array, new_array.T), axis = 1)
    print('hi')
    return array_new
  
### PROGRAM ###
m_TOT, m_PAY, m_AVC, m_PCS, cl_cruise, V, E, b, taper, cd0, U_den, Eff_Bat, Eff_Prop, rho, g = read_xlsx_input_data()
if taper == 0.45:
    e = 0.95
else:
    raise Exception

W_TOT = m_TOT * g
S = W_TOT / ( cl_cruise*V**2*rho*0.5)
MAC = S / b 
A = b**2/S
cd_cruise = cd0 + cl_cruise ** 2 / (np.pi * A * e) 
print (cd_cruise)

P_req_cruise = Eff_Prop * V * cd_cruise * W_TOT / cl_cruise
E_req_cruise = P_req_cruise * E * Eff_Bat
m_bat = E_req_cruise/U_den 

mu = 1.789*10**-5   #Pa x s

Re = rho * MAC * V / mu

print(cl_cruise/cd_cruise)
print (np.sqrt(np.pi*A*e*cd0))

    
""" 
if PRINT:
    df = pd.DataFrame(array)
    df.to_excel(print_file, sheet_name = sheet_name) 
   """
