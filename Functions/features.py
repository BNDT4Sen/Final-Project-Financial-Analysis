import pandas as pd

# Takes the current assets and current liabilities from the balance sheet to calculate the current ratio.
# This ratio indicates how readily a company is able to pay off its short-term debt.
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

# Takes the net cash flow from the cash flow statement and the current liabilities from the balance sheet.
# The operating cash flow ratio is used to determine whether or not the company can cover its short-term debt with
# cash (& cash equivalents) available in the period (in this case annually).
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

# Takes the total liabilities and total equity values from the balance sheet to calculate the debt-to-equity ratio.
# This is used to give a general sense of how leveraged a company is. Low values trending towards 0 may indicate
# that the company is underleveraged, whereas excessively high values would imply the opposite.
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

# Takes the company's earnings before income tax as well as the interest expense from the income statement.
# These are used to determine interest_coverage, which is another indicator of how relatively leveraged a company is.
# A higher value would indicate that the company's interest payments are manageable on a period to period basis.
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

# Takes both the cost of revenue and total revenues lines from the income statement to calculate operating margin.
# Operating margin reveals how much profit is made in regards to the cost of generating revenue. 
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

# Takes net income from the income statement and total assets from the balance sheet to calculate the return on assets.
# This shows how efficiently a company uses its resources to generate a profit. A higher percentage is better.
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

# Takes net income from the income statement and total equity from the balance sheet to calculate return on equity.
# Similar to return on assets, but due to adding liabilities into the equation it can be seen as more descriptive.
def return_on_equity(income_statement_df, balance_sheet_df):
    income_statement_df = income_statement_df[income_statement_df.index.isin(balance_sheet_df.index)]
    balance_sheet_df = balance_sheet_df[balance_sheet_df.index.isin(income_statement_df.index)]
    ratio_list = []
    index_list = []
    for index, row in income_statement_df.iterrows():
        net_income = row['net_income_loss']
        total_equity = balance_sheet_df.loc[index]['equity'] 
        index_list.append(index)
        ratio = net_income / total_equity
        ratio_list.append(ratio)
    ratio_series = pd.Series(data = ratio_list, index = index_list)
    return ratio_series

# Conducting some final cleaning on the combined features DataFrame. 
def final_df_check(feature_df):
    # Dropping null values and checking each column for ratios of 0, an over abundance of which could be misleading.
    print(feature_df.info())
    feature_df = feature_df.dropna().copy()
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