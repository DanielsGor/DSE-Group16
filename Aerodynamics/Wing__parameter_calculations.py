import numpy as np 
import pandas as pd
import openpyxl

read_file = write_file = 'Aerodynamics/Aerodynamic parameters.xlsx'
read_sheet = 'Inputs'
write_sheet = 'Outputs'
PRINT = False

def read_xlsx_input_data (file = read_file):
    file = pd.ExcelFile(file)
    dat = pd.read_excel(file, sheet_name = read_sheet).to_numpy() #TODO: update 
    dict = {}
    for idx, columntitles in enumerate(dat[:, 1]):
        dict[columntitles] = dat[idx,3]
    return dict

def write_to_file (output_dict, file = write_file):
    xfile = openpyxl.load_workbook(file)
    sheet = xfile.get_sheet_by_name(write_sheet)
    for idx,parameter in enumerate(output_dict):
        print (idx,parameter)
        sheet['A'+str(idx+1)] = parameter
        sheet['B'+str(idx+1)] = output_dict[parameter]
    xfile.save(file)
    return

i = read_xlsx_input_data()
o = {}

write_to_file(output_dict=o)

if PRINT:
    pass

