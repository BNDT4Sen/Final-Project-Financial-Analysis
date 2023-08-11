import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

full_df_list = ['comprehensive_income_df', 'income_statement_df', 'cash_flow_df', 'balance_sheet_df', 'filing_information_df', 'company_information_df']
statements_list = ['comprehensive_income_df', 'income_statement_df', 'cash_flow_df', 'balance_sheet_df']
other_information_list = ['filing_information_df', 'company_information_df']

def unique_check(df):
    # g3 = pd.DataFrame()
    for column in df:
        g = df.groupby(df.index)[column].value_counts()
        g2 = g[g>1]
        # pd.concat([g3, g2])
    return g2

    # unique_index = pd.unique(df.index)
    # df_difference = len(df) - len(unique_index)
    # print(f'{df_difference}')
        
def nan_check(df_list):
    series_list = []
    name_count = -1
    for df in df_list:
        column_list = []
        nan_list = []
        for column in df:
            nan_count = df[column].isna().sum()
            if nan_count > 0:
                nan_list.append(nan_count)
                column_list.append(column)
        nan_series = pd.Series(data = nan_list, index = column_list).sort_values(ascending = False)
        series_list.append(nan_series)
    for statement_series in series_list:
        name_count +=1
        df_name = statements_list[name_count]
        print(f'############{df_name}############')
        for line_item_index, line_item in statement_series.items():
            print(f'{line_item} null values in column {line_item_index}')
    return 

def year_distribution(series):
    sns.set_theme(style='darkgrid')
    sns.histplot(
        series, stat = 'proportion', discrete = True, binrange = [2009, 2022], element = 'step'
        )
    
def company_value_distribution(series):
    plt.figure(figsize = (10, 4))
    sns.set_theme(style='darkgrid')
    ax = sns.histplot(x = series, stat = 'proportion', discrete = True, shrink = 0.8)
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 30, ha = 'right')