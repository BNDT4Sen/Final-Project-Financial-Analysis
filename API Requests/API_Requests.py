import requests
import os
import pandas as pd
import json
StandardAndPoor_df = pd.read_csv('./Data/S&P 500.csv')

ticker_list = list(StandardAndPoor_df['Symbol'])

technology_125_list = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'NVDA', 
               'META', 'TSLA', 'AVGO', 'ORCL', 'ADBE', 
               'CSCO', 'CRM', 'NFLX', 'AMD', 'TXN', 
               'INTC', 'INTU', 'IBM', 'QCOM', 'AMAT', 
               'BKNG', 'NOW', 'ADP', 'ADI', 'LRCX', 
               'UBER', 'ABNB', 'FI', 'MU', 'EQIX', 
               'ATVI', 'PYPL', 'KLAC', 'VMW', 'SNPS', 
               'PANW', 'CDNS', 'WDAY', 'ANET', 'SNOW', 
               'MRVL', 'ROP', 'MCHP', 'FTNT', 'ON', 
               'ADSK', 'TTD', 'IQV', 'DELL', 'SQ', 
               'PLTR', 'CRWD', 'FIS', 'DDOG', 'EA', 
               'CSGP', 'DASH', 'GFS', 'HPQ', 'GPN', 
               'VEEV', 'SYM', 'KEYS', 'MDB', 'ALGN', 
               'ANSS', 'MPWR', 'HUBS', 'TTWO', 'EBAY', 
               'HPE', 'NET', 'FICO', 'ZS', 'ZM', 
               'COIN', 'ENPH', 'SMCI', 'SWKS', 'SNAP', 
               'SPLK', 'PTC', 'PAYC', 'NTAP', 'FDS', 
               'EXPE', 'TYL', 'ENTG', 'BSY', 'U', 
               'AKAM', 'EPAM', 'DT', 'SSNC', 'CHWY', 
               'TRMB', 'GEN', 'IOT', 'LDOS', 'Z', 
               'LSCC', 'ZBRA', 'JKHY', 'ROKU', 'AZPN', 
               'MTCH', 'OKTA', 'MANH', 'PCTY', 'PSTG', 
               'CDAY', 'TWLO', 'XM', 'GDDY', 'APP', 
               'TOST', 'DOX', 'DOCU', 'QRVO', 'HOOD', 
               'ETSY', 'CFLT', 'DBX', 'FFIV', 'W']

API_Key = os.environ['POLYGON_API_KEY']

URL = 'https://api.polygon.io/vX/reference/financials'

headers = {
    'Authorization': 'Bearer %s' % API_Key
}

Error_Count = 0
Error_List = []

for ticker in ticker_list:
    params = {
        'ticker': ticker,
        'filing_date.gte': '2010-01-01',
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

    try:
        file_name = temp_Json['results'][0]['tickers'][-1]
        file_name = ticker
        print(f'Request for {ticker}: {response.status_code}')

    except:
        file_name = 'Error'
        print(f'Error for: {ticker}')
        Error_Count += 1
        Error_List.append(ticker)

    with open(f'./Data/Raw Request Data/{file_name}_Annual_Financials.json', 'w') as outfile:
        json.dump(temp_Json, outfile)



with open('./Data/Raw Request Data/AMD_Annual_Financials.json') as json_file:
    data = json.load(json_file)

print('#'*100)
print(f'Number of stocks unavailable: {Error_Count}')
print(f'Stocks Unavailable: {Error_List}')
print('#'*100)
print('Example Data:')
print(data)
print('#'*100)