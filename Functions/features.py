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

def operating_cash_flow(cash_flow_df, balance_sheet_df):
    cash_flow_df = cash_flow_df[cash_flow_df.index.isin(balance_sheet_df.index)]
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

def interest_coverage(income_statement_df):
    ratio_list = []
    index_list = []
    for index, row in income_statement_df.iterrows():
        EBIT = row['operating_income_loss']
        interest_expense = row['interest_expense_operating']
        index_list.append(index)
        if interest_expense > 0:
            ratio = EBIT / interest_expense
        else:
            ratio = 0
        ratio_list.append(ratio)
    ratio_series = pd.Series(data = ratio_list, index = index_list)
    return ratio_series


# def asset_turnover(income_statement_df, balance_sheet_df):
#     income_statement_df = income_statement_df[income_statement_df.index.isin(balance_sheet_df.index)]
#     balance_sheet_df = balance_sheet_df[balance_sheet_df.index.isin(income_statement_df.index)]
#     ratio_list = []
#     index_list = []
#     for index, row in income_statement_df.iterrows():
#         net_sales = row['revenues']
#         # Total assets are used in place of average assets over the period due to inconsistencies between companies.
#         # The resulting ratios are very similar, and often identical, to what they would have otherwise been.
#         total_assets = balance_sheet_df.loc[index]['assets'] 
#         index_list.append(index)
#         ratio = net_sales / total_assets
#         ratio_list.append(ratio)
#     ratio_series = pd.Series(data = ratio_list, index = index_list)
#     return ratio_series

def operating_margin(income_statement_df):
    ratio_list = []
    index_list = []
    for index, row in income_statement_df.iterrows():
        cost_of_revenue = row['cost_of_revenue']
        revenues = row['revenues']
        index_list.append(index)
        if revenues > 0:
            ratio = (revenues - cost_of_revenue) / revenues
        else:
            ratio = 0
        ratio_list.append(ratio)
    ratio_series = pd.Series(data = ratio_list, index = index_list)
    return ratio_series

def return_on_assets(income_statement_df, balance_sheet_df):
    income_statement_df = income_statement_df[income_statement_df.index.isin(balance_sheet_df.index)]
    balance_sheet_df = balance_sheet_df[balance_sheet_df.index.isin(income_statement_df.index)]
    ratio_list = []
    index_list = []
    for index, row in income_statement_df.iterrows():
        net_income = row['net_income_loss']
        total_assets = balance_sheet_df.loc[index]['assets'] 
        index_list.append(index)
        ratio = net_income / total_assets
        ratio_list.append(ratio)
    ratio_series = pd.Series(data = ratio_list, index = index_list)
    return ratio_series

def return_on_equity(income_statement_df, balance_sheet_df):
    income_statement_df = income_statement_df[income_statement_df.index.isin(balance_sheet_df.index)]
    balance_sheet_df = balance_sheet_df[balance_sheet_df.index.isin(income_statement_df.index)]
    ratio_list = []
    index_list = []
    for index, row in income_statement_df.iterrows():
        net_income = row['net_income_loss']
        total_assets = balance_sheet_df.loc[index]['equity'] 
        index_list.append(index)
        ratio = net_income / total_assets
        ratio_list.append(ratio)
    ratio_series = pd.Series(data = ratio_list, index = index_list)
    return ratio_series

# def price_to_earnings(): # Will need to retrieve stock information from another API request

def final_df_check(feature_df):
    # Dropping null values and checking each column for ratios of 0, which could be misleading.
    print(feature_df.info())
    feature_df = feature_df.dropna()
    column_list = feature_df.columns
    for column in column_list:
        zero_count = feature_df[column].loc[feature_df[column] == 0].count()
        print(f'The column {column} has {zero_count} rows with values of zero!')
    # Adding another column indicating whether or not the company pays any interest. 
    interest_status = []
    for index, row in feature_df.iterrows():
        if row['interest_coverage'] > 0:
            interest_status.append(1)
        else:
            interest_status.append(0)   
    feature_df['has_interest_payments'] = interest_status

    return feature_df