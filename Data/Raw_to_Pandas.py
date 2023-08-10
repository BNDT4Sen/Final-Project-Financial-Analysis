import pandas as pd
import json
import re 

company_ticker_df = pd.read_csv('./Data/Pandas_DataFrames/Company_Ticker_DF.csv')

Missing_Count = 0
Misstatement_Count = 0

test_list = ['INTC', 'ORCL', 'IBM']


comprehensive_income_df = pd.DataFrame()

income_statement_df = pd.DataFrame()

cash_flow_df = pd.DataFrame()

balance_sheet_df = pd.DataFrame() 

# for ticker in company_ticker_df['Ticker']:
for ticker in test_list:
    try:
        with open(f'./Data/Raw Request Data/{ticker}_Annual_Financials.json') as financials:
            financials_json = json.load(financials)
            financials_df = pd.DataFrame(financials_json['results'])
            financials_stripped = financials_df[['id', 'financials', 'fiscal_year']]
            financials_stripped.set_index('id', inplace = True)
            
            print(f'{ticker} data found!')

            for index, rows in financials_stripped.iterrows():
                financial_statement_list = []
                company_information = {'ticker': ticker,
                                       'fiscal_year': financials_stripped['fiscal_year'][index]}
                for statement_name, statement_values in financials_stripped['financials'][index].items():
                    financial_dict = {}
                    financial_data = {}
                    
                    financial_statement_list.append(str(statement_name))
                    column_names = []
                    for line_item, line_value in statement_values.items():
                        column_names.append(line_item)
                        for key, value in line_value.items():
                            if key == 'value':
                                financial_data[line_item] = value

                    statement_series = pd.Series(data = financial_data, name = index)
                    information_series = pd.Series(data = company_information, name = index)

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

                    else:
                        print('Error detecting statement type!')
                        Misstatement_Count += 1
                        continue

    except FileNotFoundError:
        print(f'{ticker} data not found. :(')
        Missing_Count += 1

comprehensive_income_df.to_csv('./Data/Pandas_DataFrames/comprehensive_income_df.csv')

income_statement_df.to_csv('./Data/Pandas_DataFrames/income_statement_df.csv')

cash_flow_df.to_csv('./Data/Pandas_DataFrames/cash_flow_df.csv')

balance_sheet_df.to_csv('./Data/Pandas_DataFrames/balance_sheet_df.csv')

print(cash_flow_df)
print(f'{Missing_Count} stocks without data.')
print(f'{Misstatement_Count} financial statements could not be properly identified!')
