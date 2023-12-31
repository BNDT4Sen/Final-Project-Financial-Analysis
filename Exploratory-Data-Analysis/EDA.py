import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

full_df_list = ['comprehensive_income_df', 'income_statement_df', 'cash_flow_df', 'balance_sheet_df', 'filing_information_df', 'company_information_df']
statements_list = ['comprehensive_income_df', 'income_statement_df', 'cash_flow_df', 'balance_sheet_df']
other_information_list = ['filing_information_df', 'company_information_df']

# Checking for values that are not unique, i.e. have more than 1 occurence. 
def unique_check(df):
    for column in df:
        g = df.groupby(df.index)[column].value_counts()
        g2 = g[g>1]
    return g2.head(5)

# Removing all duplicate values after their first appearance in the DataFrame.
def duplicate_removal(df):
    df = df[~df.index.duplicated(keep = 'first')]
    return df

# Checking for null values in all of the DataFrames. Each column of each DataFrame is iterated on to retrieve the 
# number of null values. This data is then combined into a list of series which is then printed out.
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
        nan_series = pd.Series(data = nan_list, index = column_list, dtype = 'float64').sort_values(ascending = False)
        series_list.append(nan_series)
    for statement_series in series_list:
        name_count +=1
        df_name = statements_list[name_count]
        print(f'#'*25, {df_name}, '#'*25)
        for line_item_index, line_item in statement_series.items():
            print(f'{line_item} null values in column {line_item_index}')
    return 

# Most columns were found to have either no values of 0 or several thousand. The outliers in the middle include
# values that will be later used for feature engineering, and so the rows are dropped as outliers.
def drop_incomplete_rows(df):
    criteria_columns = []
    rows_to_drop = []
    for column in df:
        nan_count = df[column].isna().sum()
        if nan_count > 0 and nan_count < 100:
            criteria_columns.append(column)
    for index, row in df.iterrows():
        for dropping_column in criteria_columns:
            if np.isnan(df.loc[index][dropping_column]):
                rows_to_drop.append(index)
    print(rows_to_drop)
    print(criteria_columns)
    df = df.drop(labels = rows_to_drop)
    return df

# Returns a proportional histogram of the years for the series of filings.
def year_distribution(series):
    sns.set_theme(style='darkgrid')
    sns.histplot(
        series, stat = 'proportion', discrete = True, binrange = [2009, 2022], element = 'step'
        )

# Returns a simple visual distribution of the government offices that each company is under the jurisdiction of.
def company_value_distribution(series):
    plt.figure(figsize = (10, 4))
    sns.set_theme(style='darkgrid')
    ax = sns.histplot(x = series, stat = 'proportion', discrete = True, shrink = 0.8)
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 30, ha = 'right')

# Returns the top 12 industries by the number of companies that constitute them.
def top_industries(series):
    proportion = series.value_counts()
    proportion = proportion[proportion.values > 35]
    print(proportion)
    plt.figure(figsize = (10, 4))
    sns.set_theme(style='darkgrid')
    ax = sns.histplot(x = proportion.index, y = proportion.values, discrete = True, shrink = 0.8)
    ax.set_xticklabels(ax.get_xticklabels(), rotation = 30, ha = 'right')