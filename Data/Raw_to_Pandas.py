import pandas as pd
import numpy as np
import json

# Reading in the data for both the list of companies and the SEC industry classification list.
company_ticker_df = pd.read_csv('./Data/Company_Ticker_DF.csv')
industry_classification_df = pd.read_csv('./Data/Standard_Industrial_Classifications.csv', index_col = 'SIC Code')

# Initializing counters for potential errors that may be encountered.
Missing_Count = 0
Misstatement_Count = 0
SIC_Missing = 0
Missing_Info = 0

# Initializing the empty DataFrames to be filled.
comprehensive_income_df = pd.DataFrame()

income_statement_df = pd.DataFrame()

cash_flow_df = pd.DataFrame()

balance_sheet_df = pd.DataFrame() 

filing_information_df = pd.DataFrame()

company_information_df = pd.DataFrame()

# Each ticker is iterated over to access their respective Json file and retrieve required data.
for ticker in company_ticker_df['Ticker']:
    try:
        with open(f'./Data/Raw Request Data/{ticker}_Annual_Financials.json') as financials:
            financials_json = json.load(financials)
            financials_stripped = pd.DataFrame(financials_json['results'])
            try: # Retrieving the industry code for each company.
                industry_code = np.int64(financials_stripped['sic'])
                industry_classification = industry_classification_df.loc[industry_code]
            except: # If the industry cannot be retrieved the error is recorded.
                print('SIC code could not be retrieved')
                SIC_Missing += 1
            financials_stripped.set_index('id', inplace = True)
            print(f'{ticker} data found!')
            # The raw json for each company is iterated on by index and row.
            for index, rows in financials_stripped.iterrows():
                financial_statement_list = []
                basic_information = {'ticker': ticker,
                                       'fiscal_year': financials_stripped['fiscal_year'][index]}
                # The financial data is now combed over, retrieving a separate set of data for each financial statement.
                for statement_name, statement_values in financials_stripped['financials'][index].items():
                    # Dictionaries are initialized for the financial data that will later be converted into DataFrames.
                    financial_dict = {}
                    financial_data = {}
                    financial_statement_list.append(str(statement_name))
                    column_names = []
                    # Each the name and value for each line item in the statement is retrieved. 
                    for line_item, line_value in statement_values.items():
                        column_names.append(line_item)
                        for key, value in line_value.items():
                            if key == 'value':
                                financial_data[line_item] = value
                    # The financial statement data in addition to other company information are converted into Pandas Series.
                    statement_series = pd.Series(data = financial_data, name = index)
                    information_series = pd.Series(data = basic_information, name = index)
                    # The series are then appended to their respective DataFrames, determined by the name of the statement.
                    if statement_name == 'comprehensive_income':
                        comprehensive_concat = pd.concat(objs = [information_series, statement_series])
                        comprehensive_income_df = pd.concat(objs = [comprehensive_income_df, comprehensive_concat.to_frame().T])
                        
                    elif statement_name == 'income_statement':
                        income_concat = pd.concat(objs = [information_series, statement_series])
                        income_statement_df = pd.concat(objs = [income_statement_df, income_concat.to_frame().T])
                    
                    elif statement_name == 'cash_flow_statement':
                        cash_concat = pd.concat(objs = [information_series, statement_series])
                        cash_flow_df = pd.concat(objs = [cash_flow_df, cash_concat.to_frame().T])

                    elif statement_name == 'balance_sheet':
                        balance_concat = pd.concat(objs = [information_series, statement_series])
                        balance_sheet_df = pd.concat(objs = [balance_sheet_df, balance_concat.to_frame().T])
                    # This was set as a safeguard, but was not raised at any point for the ~ 3000 companies.
                    else:
                        print('Error detecting statement type!')
                        Misstatement_Count += 1
                        continue
                # Two additional DataFrames besides the financial statements are created.
                # Filing information provides additional data for each filing made to the SEC. 
                filing_information = {
                    'ticker': ticker,
                    'start_date': financials_stripped['start_date'][index],
                    'end_date': financials_stripped['end_date'][index],
                    'filing_date': financials_stripped['filing_date'][index],
                    'fiscal_year': financials_stripped['fiscal_year'][index],
                    'time_frame': financials_stripped['timeframe'][index],
                    'source_filing_url': financials_stripped['source_filing_url'][index]}
                filing_information_series = pd.Series(data = filing_information, name = index)
                filing_information_df = pd.concat(objs = [filing_information_df, filing_information_series.to_frame().T])
            try:
                # Company information provides categorical data relevant to the respective companies.
                company_information = {
                    'company_name': financials_stripped['company_name'][0],
                    'sic': industry_classification.index[0],
                    'office': industry_classification['Office'].values[0],
                    'industry': industry_classification['Industry Title'].values[0],
                    'cik': financials_stripped['cik'][0]}
                company_information_series = pd.Series(data = company_information, name = ticker)
                company_information_df = pd.concat(objs = [company_information_df, company_information_series.to_frame().T])
            except:
                # This error was not encountered either, all tickers had available company information.
                print(f'Company information for {ticker} could not be retrieved!')
                Missing_Info +=1
    # Some companies have changed their ticker or otherwise have had several tickers at certain periods of time.
    # Because of this, around ~ 100 companies were left out of the created DataFrames.
    # Inconsistent labelling between sources makes this a difficult problem to rectify, and with ~ 2900 companies still left, I decided to proceed regardless.
    except FileNotFoundError:
        print(f'{ticker} data not found. :(')
        Missing_Count += 1

# The concatenated DataFrames are exported into the Data folder for cleaning and EDA.
comprehensive_income_df.to_csv('./Data/Pandas_DataFrames/comprehensive_income_df.csv')

income_statement_df.to_csv('./Data/Pandas_DataFrames/income_statement_df.csv')

cash_flow_df.to_csv('./Data/Pandas_DataFrames/cash_flow_df.csv')

balance_sheet_df.to_csv('./Data/Pandas_DataFrames/balance_sheet_df.csv')

filing_information_df.to_csv('./Data/Pandas_DataFrames/filing_information_df.csv')

company_information_df.to_csv('./Data/Pandas_DataFrames/company_information_df.csv')

# Summary of the operation.
print(cash_flow_df)
print(f'{Missing_Count} stocks without data.')
print(f'{Misstatement_Count} financial statements could not be properly identified!')
print(f'Shape of comprehensive income DataFrame is: {comprehensive_income_df.shape}')
print(f'Shape of income statement DataFrame is: {income_statement_df.shape}')
print(f'Shape of cash flow DataFrame is: {cash_flow_df.shape}')
print(f'Shape of balance sheet DataFrame is: {balance_sheet_df.shape}')
print(f'Shape of filing information DataFrame is: {filing_information_df.shape}')
print(f'Shape of company information DataFrame is: {company_information_df.shape}')
print(filing_information_df)
print(company_information_df)

# Results from the following test set:

# test_set = ['INTC', 'ORCL', 'IBM']

# 0 stocks without data.
# 0 financial statements could not be properly identified!
# Shape of comprehensive income DataFrame is: (36, 7)
# Shape of income statement DataFrame is: (36, 31)
# Shape of cash flow DataFrame is: (36, 11)
# Shape of balance sheet DataFrame is: (36, 17)
# Shape of filing information DataFrame is: (36, 7)
# Shape of company information DataFrame is: (3, 5)