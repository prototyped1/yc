"""
This module allows inputs and outputs the files
"""

import sys
import os
import pandas as pd
def read_file(path = r'/data/', filename = r'Sample Super Data.xlsx'):
    if not os.path.isdir(path):
        print("Error: path does not exist.")
        sys.exit()

    full_path = os.path.join(path, filename)
    
    if not os.path.isfile(os.path.join(full_path)):
        print("Error: file does not exist.")
        sys.exit()

    print(f"Reading file from: {full_path}")
    df_disburse = pd.read_excel(full_path, sheet_name="Disbursements")
    df_payslip = pd.read_excel(full_path, sheet_name="Payslips")   
    df_paycodes = pd.read_excel(full_path, sheet_name="PayCodes")   

    return df_disburse, df_payslip, df_paycodes
    
def main():
    print("This is a pipeline for calculating super.\n")
    print("Please enter your file path (ENTER for default):")
    print("Default path: ./data/\n")

    path = input()
    if path == "":
        path = "./data/"

    print("Please enter your filename (ENTER for default):")
    print("Default filename: Sample Super Data.xlsx\n")
    filename = input()
    if filename == "":
        filename = "Sample Super Data.xlsx"

    df_disburse, df_payslip, df_paycodes = read_file(path, filename)
    print(disburse)

if __name__ == "__main__":
    main()