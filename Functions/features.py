import pandas as pd

comprehensive_income_df = pd.read_csv('./Data/Pandas_DataFrames/comprehensive_income_df.csv', index_col = [0])

income_statement_df = pd.read_csv('./Data/Pandas_DataFrames/income_statement_df.csv', index_col = [0])

cash_flow_df = pd.read_csv('./Data/Pandas_DataFrames/cash_flow_df.csv', index_col = [0])

balance_sheet_df = pd.read_csv('./Data/Pandas_DataFrames/balance_sheet_df.csv', index_col = [0])

filing_information_df = pd.read_csv('./Data/Pandas_DataFrames/filing_information_df.csv', index_col = [0])

company_information_df = pd.read_csv('./Data/Pandas_DataFrames/company_information_df.csv', index_col = [0])

full_df_list = [comprehensive_income_df, income_statement_df, cash_flow_df, balance_sheet_df, filing_information_df, company_information_df]

statements_list = [comprehensive_income_df, income_statement_df, cash_flow_df, balance_sheet_df]
                   
other_information_list = [filing_information_df, company_information_df]

def current_ratio(balance_sheet_df):
    ratio_list = []
    index_list = []
    for index, row in balance_sheet_df.iterrows():
        current_assets = row['current_assets']
        current_liabilities = row['current_liabilities']
        ratio = current_assets / current_liabilities
        ratio_list.append(ratio)
        index_list.append(index)
    ratio_series = pd.Series(data = ratio_list, index = index_list)
    return ratio_series

# print(current_ratio(balance_sheet_df))

# print(cash_flow_df.columns)

def cash_ratio(cash_flow_df, balance_sheet_df):
    cash_flow_list = []
    current_liabilities_list = []
    ratio_list = []
    index_list = []
    for index, row in cash_flow_df.iterrows():
        net_cash_flow = cash_flow_df['net_cash_flow']
        index_list.append(index)
        cash_flow_list.append(net_cash_flow)
    for index, row in balance_sheet_df.iterrows():
        current_liabilities = balance_sheet_df['net_cash_flow']
        current_liabilities_list.append(current_liabilities)
    cash_flow_series = pd.Series(data = cash_flow_list, index = index_list)

