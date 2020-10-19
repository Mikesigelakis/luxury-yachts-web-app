

import webbrowser
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output ,State
import plotly.graph_objs as go
import dash_auth
import sys
import os
import dash_bootstrap_components as dbc
import json 
import pandas as pd
import plotly.express as px

print('1')


USERNAME_PASSWORD_PAIRS =[ ['yachtunion', 'yachtunion']]


sys.path.insert(1,'src/manipulate_data')

 
from dataframe_functions import (
    set_not_given_on_specific_columns_of_a_dataframe
   ,exports_unique_data_of_a_dataframe_from_a_column 
)

def multi_dropdown_with_label(label_name , items , multi_values):
        options = []
        the_id = ''
        the_value = ''
        if label_name  == 'PRICE':
                for value in items:
                        options.append({'label': value,'value': value })  
                        the_id = 'price-picker'
        if label_name  == 'YEAR':
                for value in items:
                        options.append({'label': value,'value': value })  
                        the_id = 'year-picker'
                        value = '2010'
        
        
        label_dropdown =[dbc.Col(html.Div(label_name), className = 'label-dropdown', width = 1)
       ,dbc.Col(dcc.Dropdown(
                options=options,
                multi=multi_values,
                id = the_id,
                value = the_value
                ))
        ]
        return label_dropdown

def bootstrap_button(label , color):
    button = dbc.Button(label , color=color ,block=True , id = 'submit-val-'+label)
    return button


 


df = pd.read_csv('data/all_data.csv')
df.drop(columns =  ['Unnamed: 0'], inplace = True)



df  = set_not_given_on_specific_columns_of_a_dataframe(df , ['Price','Link', 'Year'])

df['Price'] = df['Price'].astype('int64')
filter_price=  df['Price'] < 550000
df = df[filter_price]

unique_coutries =  exports_unique_data_of_a_dataframe_from_a_column(df, 'Country')
unique_prices =  ['300000-350000', '350000-400000', '400000-450000', '450000-500000', '500000-550000']
unique_years = [
    '2000', '2001' ,'2002', '2003', '2004' , '2005', '2006' , '2007',
    '2008', '2009' ,'2010', '2011', '2012' , '2013', '2014' , '2015', 
    '2016', '2017', '2018', '2019', '2020']

filter_year = df['Year'].isin(unique_years)
df=  df [filter_year]
 
app = dash.Dash(__name__ , external_stylesheets=[dbc.themes.BOOTSTRAP])
auth = dash_auth.BasicAuth(app , USERNAME_PASSWORD_PAIRS)
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
 
 
app.layout = html.Div(
         [  dbc.Row(dbc.Col(html.Div("FIND THE BEST YACHT" , className = "d-flex justify-content-center application-Title"))),
            dbc.Row(  
            [
                   multi_dropdown_with_label('PRICE', unique_prices, False)[0]
                  ,multi_dropdown_with_label('PRICE', unique_prices, False)[1]
                  ,multi_dropdown_with_label('YEAR', unique_years,  True)[0]
                  ,multi_dropdown_with_label('YEAR', unique_years , True)[1]

            ], className = 'form-filters-row'),
            dbc.Row(  dbc.Col(bootstrap_button('Submit', 'info' ), width={"size": 12}),className = 'form-filters-row-3'),
            dbc.Row(dbc.Col( dcc.Graph(id='graph'), width={"size": 12}), className = 'form-filters-row-2'),
            dbc.Row(
            dbc.Col(
                      dbc.Form([],className = "border-specific-car", id ='graph_2')
            , className = 'form-filters-row-4'
            , width = 3),

                   
 )           
         ]
 
 )

@app.callback(Output('graph', 'figure')
             ,[Input('submit-val-Submit', 'n_clicks')]
             ,[State('price-picker', 'value')
             ,State('year-picker', 'value')
            ]
             
               
             )
def update_figure(clicks,price, years):
    try: 
        new_df = df
        asked_years =     years 
        prices = [price]
 
        price_List =  []
        if len(price) >  0:
             new_df = pd.DataFrame(columns =  df.columns)
             for value in prices:
                 price = value.replace('-' , ' ')
                 price = price.split()
                 price = [int(price[0]),int(price[1]) ]
                 price_List.append(price)
             for value in price_List: 
                 price_filter = df['Price'].between(value[0], value[1])
                 temp_df = df[price_filter]    
                 new_df  =  new_df.append(temp_df)

         
        filter_year  =  new_df['Year'] != 'No filter'

        if  asked_years:  
            filter_year = new_df['Year'].isin(asked_years)



        new_df = new_df[ filter_year] 



        fig = px.scatter(new_df, x='Price', y="Year"
                     ,hover_data =  ['Link','Title', 'Year', 'Price','Location' ]  
                     ,color  = 'Country'
                     ,title = 'Diagram'
                     ,color_discrete_sequence=['#D6278B','#636EFA' ,'#00DD96' , '#555632', '#415'] 
                         )
        fig.update_layout(
            hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Rockwell"    
            ))

        return fig    
    except Exception as e: 
            print(e)
        
            return {
                "layout": {
                    "xaxis": {
                        "visible": False
                    },
                    "yaxis": {
                        "visible": False
                    },
                    "annotations": [
                        {
                            "text": "No matching data found",
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": False,
                            "font": {
                                "size": 28
                            }
                        }
                    ]
                }
            }


@app.callback(Output('graph_2', 'children'), [Input('graph', 'clickData')])
def disp_hover_data(clickData):
    if clickData != None:
        return_specific_car =  [
             dbc.FormGroup([
                    dbc.Badge('Link',color="light",className ='information-specific-car-label')
                   ,html.Label(html.A(str(clickData['points'][0]['customdata'][0]) , href=str(clickData['points'][0]['customdata'][0]),target='_blank'),className ='information-specific-car')
        ])]
        
        a_website = clickData['points'][0]['customdata'][0]
        webbrowser.open_new_tab(a_website)
        
        columns_for_car = ['Title','Year','Price','Location']         
        for index, value in enumerate(columns_for_car): 
            return_specific_car.append( dbc.FormGroup([
                    dbc.Badge(value,color="light",className ='information-specific-car-label')
                   ,dbc.Label(str(clickData['points'][0]['customdata'][index+1]),className ='information-specific-car')
                 ]

                )
            )
        return  return_specific_car



application = app.server 
if __name__ == '__main__':
    application.run(debug=True, port=8080)
