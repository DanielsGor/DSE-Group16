import numpy as np 
import pandas as pd
import openpyxl

read_file = ^'Aerodynamics/Aerodynamic parameters.xlsx' #TODO:e
write_file = 0
read_sheet = 'Inputs'
write_sheet = 'Outputs'
PRINT = False

def read_xlsx_input_data (file = read_file):
    file = pd.ExcelFile(file)
    dat = pd.read_excel(file, sheet_name = read_sheet).to_numpy() #TODO: update 
    dict = {}
    for idx, columntitles in enumerate(dat[1, :]):
        dict[columntitles] = dat[3:, idx]
    return dict

# def write_to_file (file = write_file, variable, value):
#     xfile = openpyxl.load_workbook('test.xlsx')
#     sheet = xfile.get_sheet_by_name('Sheet1')
#     sheet['A1'] = 'hello world'
#     xfile.save('text2.xlsx')
#     return

