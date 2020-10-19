import pandas as pd 


def set_not_given_on_specific_columns_of_a_dataframe(df, columns):
    for column in columns: 
        mask = df[column] != 'Not Given'
        df =df[mask]  
    return df 
def exports_unique_data_of_a_dataframe_from_a_column(df, column_name, countries = ['Greece', 'Croatia', 'France','Italy', 'Spain']):
    options = []
    
    filter_country = df['Country'].isin(countries)
    df = df[filter_country]
    
    for value in df[column_name].unique():
        options.append(value)
    options.sort(reverse = True)
    return options






 

  