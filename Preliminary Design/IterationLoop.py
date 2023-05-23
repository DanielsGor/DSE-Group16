import pandas as pd
import numpy as np

#constants
g = 9.81
rho = 1.225

#file constants
file = "Preliminary Design\Preliminary design.xlsx"
sheet_name = "Class_1_New"

# xlsx file processing
def load_xlsx_input_data(file):
    file = pd.ExcelFile(file)
    
    dat = pd.read_excel(file, sheet_name).to_numpy() [1:10,1]
    return dat

def write_xlsx_file ():
    array_old = pd.read_excel(file, sheet_name).to_numpy()
    print (array_old)
    return
payload, V, T, b, cl_cruise, cd_cruise, e_density, tot_eff, tot_mass = load_xlsx_input_data(file)


tot_weight = tot_mass*g/1000
S = tot_weight/ ( cl_cruise*V**2*rho*0.5)
wingLoading = tot_weight/S
MAC = S / b #for no sweep
P_req = V * cd_cruise * tot_weight/cl_cruise
E_tot = P_req * T/60
E_tot_eff = E_tot/tot_eff
m_bat = E_tot_eff/e_density
#TODO: calc total weight

write_xlsx_file()


