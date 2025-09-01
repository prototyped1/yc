This Python pipeline calculates superannuation payable and compares it with actual disbursements based on employee payslip data. It reads from an Excel file containing three sheets and outputs a CSV file showing variances per employee per quarter.


Input Excel File (default: Sample Super Data.xlsx)

Disbursements: Records of super payments made

Payslips: Employee payslip data

PayCodes: Mapping of pay codes and their OTE treatment


Output File

results.csv: Contains merged data with calculated super payable, disbursed amounts, and variance


How to Run

Run the script via CLI:

python calcsuper_yc.py


You’ll be prompted to enter:

File path (default: ./data/)

Filename (default: Sample Super Data.xlsx)


Modules

1. read_file(path, filename)

Validates path and file existence

Reads three sheets from the Excel file using pandas


2. calc_ote(df_payslip, df_paycodes)

Identifies OTE-relevant pay codes

Filters payslip entries based on OTE codes

Aggregates OTE amounts by employee, year, and quarter

Calculates super payable (default rate: 9.5%)


3. calc_disb(df_disburse)

Aggregates disbursed super amounts by employee, year, and quarter


4. main()

Handles CLI interaction

Merges OTE and disbursement data

Calculates variance

Saves final results to CSV


Dependencies

Python 3.x

pandas


Notes
Ensure the Excel file contains the correct sheet names.

Super rate is currently hardcoded at 9.5%. Update as needed.
