import pandas as pd

# comprehensive_income_df = pd.read_csv('./Data/Cleaned_Pandas_DataFrames/comprehensive_income_df.csv', index_col = [0])

# income_statement_df = pd.read_csv('./Data/Cleaned_Pandas_DataFrames/income_statement_df.csv', index_col = [0])

# cash_flow_df = pd.read_csv('./Data/Cleaned_Pandas_DataFrames/cash_flow_df.csv', index_col = [0])

# balance_sheet_df = pd.read_csv('./Data/Cleaned_Pandas_DataFrames/balance_sheet_df.csv', index_col = [0])

# filing_information_df = pd.read_csv('./Data/Cleaned_Pandas_DataFrames/filing_information_df.csv', index_col = [0])

# company_information_df = pd.read_csv('./Data/Cleaned_Pandas_DataFrames/company_information_df.csv', index_col = [0])

# full_df_list = [comprehensive_income_df, income_statement_df, cash_flow_df, balance_sheet_df, filing_information_df, company_information_df]

# statements_list = [comprehensive_income_df, income_statement_df, cash_flow_df, balance_sheet_df]
                   
# other_information_list = [filing_information_df, company_information_df]

def current_ratio(balance_sheet_df):
    ratio_list = []
    index_list = []
    for index, row in balance_sheet_df.iterrows():
        current_assets = row['current_assets']
        current_liabilities = row['current_liabilities']
        if current_assets > 0 and current_liabilities > 0:
            ratio = current_assets / current_liabilities
            ratio_list.append(ratio)
            index_list.append(index)
        else:
            balance_sheet_df.drop(labels = index)
    ratio_series = pd.Series(data = ratio_list, index = index_list)
    return ratio_series

# print(current_ratio(balance_sheet_df))

# print(cash_flow_df.columns)

def operating_cash_flow(cash_flow_df, balance_sheet_df):
    balance_sheet_df = balance_sheet_df[balance_sheet_df.index.isin(cash_flow_df.index)]
    ratio_list = []
    index_list = []
    for index, cash_row in cash_flow_df.iterrows():
        net_cash_flow = cash_row['net_cash_flow']
        current_liabilities = balance_sheet_df.loc[index]['current_liabilities']
        index_list.append(index)
        ratio = net_cash_flow / current_liabilities
        ratio_list.append(ratio)
    ratio_series = pd.Series(data = ratio_list, index = index_list)
    return ratio_series

def debt_to_equity(balance_sheet_df):
    ratio_list = []
    index_list = []
    for index, row in balance_sheet_df.iterrows():
        total_liabilities = row['liabilities']
        shareholders_equity = row['equity']
        index_list.append(index)
        ratio = total_liabilities / shareholders_equity
        ratio_list.append(ratio)
    ratio_series = pd.Series(data = ratio_list, index = index_list)
    return ratio_series

