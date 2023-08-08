import pandas as pd
import tabula

# PDF file contains a list of approximately 3000 of the largest companies in the USA.
pdf_path = './Data/Russel 3000.pdf'

# Tabula can automagically detect PDF tables and return a list of DataFrames.
dfs = tabula.read_pdf(pdf_path, stream = True, encoding = 'cp1252', pages = 'all')

# A total of 31 individual DataFrames are returned.
len(dfs)

# Currently each DataFrame contains duplicate columns with differing values.
# They will need to be iterated upon and split, before being fully combined later.
df_list = []

for df in dfs:
    
    first_half_df = pd.DataFrame(data = df[['Russell 3000® Index', 'Unnamed: 0']])
    first_half_df.rename(columns = first_half_df.iloc[0], inplace = True)
    first_half_df.drop(0, inplace = True)
    df_list.append(first_half_df)
    
    second_half_df = pd.DataFrame(data = df[['Unnamed: 1', 'Unnamed: 2']])
    second_half_df.rename(columns = second_half_df.iloc[0], inplace = True)
    second_half_df.drop(0, inplace = True)
    df_list.append(second_half_df)

# The result is an expected 62 DataFrames.
print(len(df_list))

# The second last page of the Russel 3000 PDF file is an incomplete table, and Tabula cannot understand it.
# Because the number of companies remaining was only ~30, I copied them into a DataFrame manually.
last_page = [
    ['WIX.COM', 'WIX'],
    ['WM TECHNOLOGY INC (A)', 'MAPS'],
    ['WOLFSPEED INC', 'WOLF'],
    ['WOLVERINE WORLD WIDE', 'WWW'],
    ['WOODWARD', 'WWD'],
    ['WORKDAY', 'WDAY'],
    ['WORKHORSE GROUP', 'WKHS'],
    ['WORKIVA', 'WK'],
    ['WORLD ACCEPTANCE', 'WRLD'],
    ['WORLD FUEL SERVICES', 'INT'],
    ['WORTHINGTON INDS', 'WOR'],
    ['WSFS FINANCIAL CORP', 'WSFS'],
    ['WW INTERNATIONAL INC', 'WW'],
    ['WWF ENTMNT', 'WWE'],
    ['WYNDHAM HOTELS & RESORTS', 'WH'],
    ['WYNN RESORTS', 'WYNN'],
    ['XCEL ENERGY', 'XEL'],
    ['XENCOR', 'XNCR'],
    ['XENIA HOTELS & RESORTS', 'XHR'],
    ['XERIS BIOPHARMA HOLDINGS INC', 'XERS'],
    ['XEROX HOLDINGS', 'XRX'],
    ['XOMETRY', 'XMTR'],
    ['XOS INC (A)', 'XOS'],
    ['XPEL INC', 'XPEL'],
    ['XPERI HOLDING CORPORATION', 'XPER'],
    ['XPO LOGISTICS', 'XPO'],
    ['XPONENTIAL FITNESS', 'XPOF'],
    ['XYLEM INC.', 'XYL'],
    ['YELP', 'YELP'],
    ['Y-MABS THERAPEUTICS', 'YMAB'],
    ['ZUMIEZ', 'ZUMZ'],
    ['ZUORA', 'ZUO'],
    ['ZURN WATER SOLUTIONS CORPORATION', 'ZWS'],
    ['ZYNEX', 'ZYXI']
]

last_page_df = pd.DataFrame(data = last_page, columns = ['Company', 'Ticker'])
df_list.append(last_page_df)

#All 63 DataFrames are concatenated together.
Ticker_List = pd.concat(df_list)

# All 3010 rows contain unique tickers; no duplicate values.
len(Ticker_List['Ticker'].unique())

# Rows are sorted alphabetically via Ticker symbol.
Ticker_List.sort_values(by = 'Ticker', ignore_index = True, inplace = True)

# Completed Base DataFrame is exported to be used for API requests.
Ticker_List.to_csv('./Data/Company_Ticker_DF.csv', index = False)