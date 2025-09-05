

import sys
import os
import argparse
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

SUPER_RATE = 0.095
"""
This module handles inputs and outputs of the files
"""
def read_file(path, filename):
    if not os.path.isdir(path):
        print("Error: path does not exist.")
        print(path)
        sys.exit()

    full_path = os.path.join(path, filename)
    
    if not os.path.isfile(full_path):
        print("Error: file does not exist.")
        print(full_path)
        sys.exit()

    print(f"Reading file from: {full_path}")
    df_disburse = pd.read_excel(full_path, sheet_name="Disbursements")
    df_payslip = pd.read_excel(full_path, sheet_name="Payslips")   
    df_paycodes = pd.read_excel(full_path, sheet_name="PayCodes")   

    return df_disburse, df_payslip, df_paycodes
    
"""
This module handles CLI inputs and outputs
"""
def main():
    print("This is a pipeline for calculating super.\n")
   
    parser = argparse.ArgumentParser(description="Calculate superannuation from a file.")
    parser.add_argument("--filepath", help="Path to the input file (e.g., ./data/)")
    parser.add_argument("--filename", help="Name of the input file (e.g., Sample Super Data.xlsx)")
    args = parser.parse_args()

    # If arguments are missing, fall back to interactive prompts
    if not args.filepath:
        print("Please enter your file path (ENTER for default):")
        print("Default path: ./data/\n")
        path = input()
        if path == "":
            path = "./data/"
    else:
        path = args.filepath

    if not args.filename:
        print("Please enter your filename (ENTER for default):")
        print("Default filename: Sample Super Data.xlsx\n")
        filename = input()
        if filename == "":
            filename = "Sample Super Data.xlsx"
    else:
        filename = args.filename

    df_disburse, df_payslip, df_paycodes = read_file(path, filename)
    
    df_ote = calc_ote(df_payslip, df_paycodes)
    df_disbursed = calc_disb(df_disburse)

    df_final = pd.merge(df_ote, df_disbursed, how='outer', on=['employee_code','year','quarter'])
    df_final = df_final.fillna(0)
    df_final.loc[:,'Variance'] = df_final['Super Payable'].round(2) - df_final['Total Disbursed'].round(2)
    df_final.to_csv(os.path.join(path,'results.csv'), index=False)

    print(f"Results saved to {os.path.join(path,'results.csv')}")
    print("Done!")
"""
This module allows the calculation of the OTE and payable super
"""
def calc_ote(df_payslip, df_paycodes):
    # note every pay_code contrains a prefix code
    df_paycodes.loc[:,'codes'] = df_paycodes['pay_code'].str.split(' -',expand=True)[0]
    df_ote = df_paycodes.loc[df_paycodes['ote_treament']=='OTE',"codes"]

    df_payslip.loc[:,'ote_type'] = df_payslip['code'].str.split(' -',expand=True)[0]
    df_payslip_ote = df_payslip.loc[df_payslip['ote_type'].isin(df_ote),:]
    
    df_payslip_ote.loc[:,'date'] = pd.to_datetime(df_payslip_ote['end'])
    df_payslip_ote.loc[:,'year'] = df_payslip_ote['date'].dt.year
    df_payslip_ote.loc[:,'quarter'] = (df_payslip_ote['date'].dt.month-1)%12//3+1

    df_payslip_ote_sum = df_payslip_ote.groupby(['employee_code','year','quarter']).agg({'amount':'sum'}).reset_index()
    df_payslip_ote_sum = df_payslip_ote_sum.rename(columns={'amount':'Total OTE'})

    df_payslip_ote_sum.loc[:,'Super Payable'] = (df_payslip_ote_sum['Total OTE'] * SUPER_RATE).round(2)

    return df_payslip_ote_sum

"""
This module allows the calculation of the disbursements
"""
def calc_disb(df_disburse):
    df_disburse.loc[:,'date'] = pd.to_datetime(df_disburse['payment_made'])
    df_disburse.loc[:,'year'] = df_disburse['date'].dt.year
    df_disburse.loc[:,'quarter'] = (df_disburse['date'].dt.month-1)%12//3+1

    df_disburse_sum = df_disburse.groupby(['employee_code','year','quarter']).agg({'sgc_amount':'sum'}).reset_index()
    df_disburse_sum = df_disburse_sum.rename(columns={'sgc_amount':'Total Disbursed'})

    return df_disburse_sum


if __name__ == "__main__":
    main()