import sqlite3
import pandas as pd

# Each Pandas DataFrame is read in.
comprehensive_income = pd.read_csv('./Data/Pandas_DataFrames/comprehensive_income_df.csv', index_col = [0])

income_statement = pd.read_csv('./Data/Pandas_DataFrames/income_statement_df.csv', index_col = [0])

cash_flow = pd.read_csv('./Data/Pandas_DataFrames/cash_flow_df.csv', index_col = [0])

balance_sheet = pd.read_csv('./Data/Pandas_DataFrames/balance_sheet_df.csv', index_col = [0])

filing_information = pd.read_csv('./Data/Pandas_DataFrames/filing_information_df.csv', index_col = [0])

company_information = pd.read_csv('./Data/Pandas_DataFrames/company_information_df.csv', index_col = [0])

# A dictionary of the DataFrames is created.
full_df_dict = {
    'comprehensive_income': comprehensive_income, 
    'income_statement': income_statement, 
    'cash_flow': cash_flow, 
    'balance_sheet': balance_sheet, 
    'filing_information': filing_information, 
    'company_information': company_information
}

# Creating the SQLite Database
conn = sqlite3.connect('./SQL-Database/Russel_3000_Financials.db')

# Iterating on the DataFrame dictionary, converting each DataFrame into a table in the new Database.
for index, df in full_df_dict.items():
    df.to_sql(index, conn, index = True, if_exists = 'replace')
