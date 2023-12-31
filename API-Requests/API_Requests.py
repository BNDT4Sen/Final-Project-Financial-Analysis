import requests
import os
import pandas as pd
import json

# DataFrame of 3010 American Stocks is loaded.
Russel_df = pd.read_csv('./Data/Company_Ticker_DF.csv')

# Tickers of each company are collected into a list for iteration. 
ticker_list = list(Russel_df['Ticker'])

# ticker_list = ['AMD', 'INTC', 'NVDA', 'MSFT', 'AAPL'] # List for testing purposes.

# Setup of key parameters for the requests library.
API_Key = os.environ['POLYGON_API_KEY']

URL = 'https://api.polygon.io/vX/reference/financials'

headers = {
    'Authorization': 'Bearer %s' % API_Key
}

# Keeping track of the number and name of companies from which data could not be retrieved.
Error_Count = 0
Error_List = []

# Annual reports for each ticker from 2008 to 2023 are requested.
for ticker in ticker_list:
    params = {
        'ticker': ticker,
        'filing_date.gte': '2008-01-01',
        'filing_date.lt':   '2023-01-01',
        'timeframe': 'annual',
        'order': 'asc',
        'limit': 100,
        'sort': 'period_of_report_date'
    }

    response = requests.request(
    'GET', 
    URL, 
    params = params, 
    headers = headers
    )

    temp_Json = json.loads(response.text)

    # If obtaining data from a request is unsuccessful an exception is raised and keeps track of which Ticker ran into issues.
    try:
        file_name = temp_Json['results'][0]['tickers'][-1]
        file_name = ticker
        print(f'Request for {ticker}: {response.status_code}')
    except:
        file_name = 'Error'
        print(f'Error for: {ticker}')
        Error_Count += 1
        Error_List.append(ticker)

    # Each request is stored as a JSON file within the Data Folder for later processing.
    with open(f'./Data/Raw Request Data/{file_name}_Annual_Financials.json', 'w') as outfile:
        json.dump(temp_Json, outfile)

# One of the requests is tested.
with open('./Data/Raw Request Data/AMD_Annual_Financials.json') as json_file:
    data = json.load(json_file)

# A summary of the API Requests is outputted.
print('#'*100)
print(f'Number of stocks unavailable: {Error_Count}')
print(f'Stocks Unavailable: {Error_List}')
print('#'*100)
print('Example Data:')
print(data)
print('#'*100)