import pandas as pd
import numpy as np

### CONSTANTS ###
#linear model relating mass and power of propulsion system (from Louis)
m1, p1 = 0.0027, 10
m2, p2= 0.070, 200
dmdp = (m2-m1)/(p2-p1)

#margins
massMargin = 1.2
powerMargin = 1.1
energyMargin = 1.1

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
    dat = pd.read_excel(file,header = None, sheet_name = read_sheet).to_numpy() [1:18,1]
    return dat

def new_iteration (array):
    new_array = np.array(dict.items())
    array_new = np.concatenate((array, new_array.T), axis = 1)
    print('hi')
    return array_new
  
### PROGRAM ###
iteration_array = pd.read_excel(read_file, read_sheet, header =None).to_numpy() 

m, m_PAY, m_AVC, m_PCS, m_LND, cl_cruise, V, ROC, E, b, cd0, e, U_den, Eff_Bat, Eff_Prop, rho, g = read_xlsx_input_data()
m_TOT = 1.1 * m #intial guess
n_iter = 1

while np.abs(m-m_TOT) > m_TOT * convergence:
    m_TOT = m #reiteration
    #general parameter calculations
    W_TOT = m_TOT * g
    S = W_TOT / (cl_cruise * V ** 2 * rho * 0.5)
    MAC = S / b 
    A = b ** 2 / S
    cd_cruise = cd0 + cl_cruise ** 2 / (np.pi * A * e) 

    #battery values calculations
    P_req_cruise = 1 / Eff_Prop * V * cd_cruise * W_TOT / cl_cruise
    E_req_cruise = P_req_cruise * E / Eff_Bat

    #propulsion system calculations
    P_req_climb = W_TOT * ROC / Eff_Prop + P_req_cruise

    #include power and energy margin
    # E_req_cruise *= energyMargin
    # P_req_climb *= powerMargin
    
    #mass calculations
    m_PRP = m1 + (P_req_climb-p1) * dmdp
    m_EPS = E_req_cruise/U_den 
    m_STR = (m_AVC + m_PAY + m_PCS + m_EPS + m_PRP + m_LND)*35/65
    m = m_STR * 100/35
    
    #print (n_column)
    #iteration_array = new_iteration(n_iter, iteration_array) 

    # n_iter += 1

print (m)
print (cl_cruise/cd_cruise)
""" 
if PRINT:
    df = pd.DataFrame(array)
    df.to_excel(print_file, sheet_name = sheet_name) 
   """
