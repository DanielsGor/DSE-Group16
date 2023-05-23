import pandas as pd
import numpy as np

#constants
g = 9.81
rho = 1.225 
percentageConvergence = 0.0005
PRINT = False

m1, p1 = 2.7, 10
m2, p2= 70, 200
dmdp = (m2-m1)/(p2-p1)

#file constants
file = "Preliminary Design\Preliminary design.xlsx"
sheet_name = "Class_1_New"
print_file  = "Preliminary Design\Preliminary iteration.xlsx"

# xlsx file processing
def load_xlsx_input_data(file):
    file = pd.ExcelFile(file)
    
    dat = pd.read_excel(file,header = None, sheet_name = sheet_name).to_numpy() [1:10,1]
    return dat

def new_iteration (n, array):
    iterationTitle = str("Iteration "+ str(n))
    new_array = np.array([[iterationTitle, m_payload, V, T, b, cl_cruise, cd_cruise, e_density, tot_eff, m_tot, wingLoading, S, MAC, P_req, E_tot, E_tot_eff, m_bat, A, m_avionics, m_plasmaActuators, m_fuselage, m_wing, m_prop, m_empannage]])
    array_new = np.concatenate((array, new_array.T), axis = 1)
    return array_new

def write_xlsx_file (array):
    df = pd.DataFrame(array)
    df.to_excel(print_file, sheet_name = sheet_name) 
    return

#initialise system
iteration_array = pd.read_excel(file, sheet_name, header =None).to_numpy()
m_payload, V, T, b, cl_cruise, cd_cruise, e_density, tot_eff, m = load_xlsx_input_data(file)
m_tot = 1.1 * m#initial guess
n_iter = 1



while np.abs(m-m_tot) > m_tot * percentageConvergence:
    m_tot = m
    tot_weight = m_tot*g/1000
    S = tot_weight/ ( cl_cruise*V**2*rho*0.5)
    wingLoading = tot_weight/S
    MAC = S / b #for no sweep
    P_req = V * cd_cruise * tot_weight/cl_cruise
    E_tot = P_req * T/60
    E_tot_eff = E_tot/tot_eff
    m_bat = E_tot_eff/e_density
    A = b**2/S

    m_avionics = 655
    m_plasmaActuators = 245*b
    m_fuselage = 200
    m_wing = S*1000
    m_prop = m1 + (P_req/tot_eff-p1) * dmdp
    m_empannage = 28+33

    m_struc = m_fuselage + m_wing + m_empannage

    m = m_avionics + m_plasmaActuators + m_fuselage + m_wing + m_prop + m_empannage + m_bat*1000 + m_payload

    n_iter += 1
    #print (n_column)
    iteration_array = new_iteration(n_iter, iteration_array) 

print (m_struc, '\n', m_struc/m)
print (m_bat)
if PRINT:
    write_xlsx_file(iteration_array)
