import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, State, Output
import dash_bootstrap_components as dbc


def multi_dropdown_with_label(label_name , items , multi_values):
        options = []
        the_id = ''
        the_value = ''
        if label_name  == 'PRICE':
                for value in items:
                        options.append({'label': value,'value': value })  
                        the_id = 'price-picker'
        if label_name  == 'COUNTRY':
                for value in items:
                        options.append({'label': value,'value': value })  
                        the_id = 'country-picker'
        
        
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

 