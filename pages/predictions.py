# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#import joblib
from pickle import load
import pandas as pd

# Imports from this application
from app import app

# Load the model pipeline
#pipeline = joblib.load('assets/model_xgb2.pkl')
with open("assets/model_xgb2.pkl", "rb") as f:
     pipeline = load(f)

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Predictions

            Adjust the Inputs below to see which influence the 
            likelihood that your Kickstarter Campaign will meet 
            its funding goal and be Successful

            """
        ),
        dcc.Markdown('#### Main Category'), 
        dcc.Dropdown(
            id='main_category', 
            options = [
                {'label': 'Art', 'value': 'Art'}, 
                {'label': 'Comics', 'value': 'Comics'}, 
                {'label': 'Crafts', 'value': 'Crafts'}, 
                {'label': 'Dance', 'value': 'Dance'}, 
                {'label': 'Design', 'value': 'Design'},
                {'label': 'Fashion', 'value': 'Fashion'}, 
                {'label': 'Film & Video', 'value': 'Film & Video'}, 
                {'label': 'Food', 'value': 'Food'}, 
                {'label': 'Games', 'value': 'Games'}, 
                {'label': 'Journalism', 'value': 'Journalism'},
                {'label': 'Music', 'value': 'Music'},
                {'label': 'Photography', 'value': 'Photography'},
                {'label': 'Publishing', 'value': 'Publishing'},
                {'label': 'Technology', 'value': 'Technology'},
                {'label': 'Theater', 'value': 'Theater'}, 
            ], 
            className='mb-3',
        ),
        dcc.Markdown('#### Currency'), 
        dcc.Dropdown(
            id='currency', 
            options = [
                {'label': 'Australian Dollar', 'value': 'AUD'}, 
                {'label': 'British Pound', 'value': 'GBP'},
                {'label': 'Canadian Dollar', 'value': 'CAD'}, 
                {'label': 'Danish Krone', 'value': 'DKK'}, 
                {'label': 'Euro', 'value': 'EUR'},
                {'label': 'Hong Kong Dollar', 'value': 'HKD'}, 
                {'label': 'Japanese Yen', 'value': 'JPY'}, 
                {'label': 'Mexican Peso', 'value': 'MXN'}, 
                {'label': 'Norwegian Krone', 'value': 'NOK'},
                {'label': 'New Zealand Dollar', 'value': 'NZD'},
                {'label': 'Singapore Dollar', 'value': 'SGD'},
                {'label': 'Swedish Krona', 'value': 'SEK'},
                {'label': 'Swiss Franc', 'value': 'CHF'},
                {'label': 'U.S. Dollar', 'value': 'USD'},
            ], 
            className='mb-3',
        ),
        dcc.Markdown('#### Funding Goal (between 0 and 1,000,000)'), 
        dcc.Input(
            id='goal',
            placeholder='Integer Value',
            type='number',
            min=0,
            max=1000000,
            step=1,
            value='',
            className='mb-3',
        ),
        dcc.Markdown('#### Country'), 
        dcc.Dropdown(
            id='country', 
            options = [
                {'label': 'Australia', 'value': 'AU'},
                {'label': 'Austria', 'value': 'AT'}, 
                {'label': 'Belgium', 'value': 'BE'},
                {'label': 'Canada', 'value': 'CA'}, 
                {'label': 'Denmark', 'value': 'DK'}, 
                {'label': 'France', 'value': 'FR'},
                {'label': 'Germany', 'value': 'DE'},
                {'label': 'Great Britain', 'value': 'GB'},
                {'label': 'Hong Kong', 'value': 'HK'}, 
                {'label': 'Ireland', 'value': 'IE'},
                {'label': 'Italy', 'value': 'IT'},
                {'label': 'Japan', 'value': 'JP'}, 
                {'label': 'Luxembourg', 'value': 'LU'},
                {'label': 'Mexico', 'value': 'MX'}, 
                {'label': 'Netherlands', 'value': 'NL'},
                {'label': 'Norway', 'value': 'NO'},
                {'label': 'New Zealand', 'value': 'NZ'},
                {'label': 'Singapore', 'value': 'SG'},
                {'label': 'Spain', 'value': 'ES'},
                {'label': 'Sweden', 'value': 'SE'},
                {'label': 'Switzerland', 'value': 'CH'},
                {'label': 'United States', 'value': 'US'},
            ], 
            className='mb-3', 
        ),
        dcc.Markdown('#### Campaign Duration (in Days)'), 
        dcc.Slider(
            id='duration_days', 
            min=1,
            max=92,
            step=1, 
            value=1, 
            marks={1 : '1',
                   30: '30',
                   60: '60',
                   92: '92'}, 
            className='mb-3', 
        ), 
    ],
    md=6,
)

column2 = dbc.Col(
    [
        html.H2('Expected Campaign Result:', className='mb-5', 
                 style={'textAlign': 'center'}), 
        html.Div(id='prediction-content', className='lead', 
                 style={'textAlign': 'center', 'font-weight': 'bold'}),
        html.Div(id='prediction-image')
    ],

    md = 4
)

@app.callback(
    Output('prediction-content', 'children'),
    [Input('main_category', 'value'), Input('currency', 'value'),
     Input('goal', 'value'), Input('country', 'value'), 
     Input('duration_days', 'value')],
)
def predict(main_category, currency, goal, country, duration_days):
    df = pd.DataFrame(
        columns=['main_category', 'currency', 'goal', 'country', 
                 'duration_days'], 
        data=[[main_category, currency, goal, country, duration_days]]
    )
    y_pred = pipeline.predict(df)[0]
    if y_pred == 1:
        return f'Congratulations! Your Kickstarter Campaign Was \
            Successfuly Funded!'
    else:
        return f'We Are Sorry But Your Kickstarter Campaign Was Not\
            Successfuly Funded! Please revise your inputs and try again!'

@app.callback(
    Output('prediction-image', 'children'),
    [Input('main_category', 'value'), Input('currency', 'value'),
     Input('goal', 'value'), Input('country', 'value'), 
     Input('duration_days', 'value')],
)
def predict_image(main_category, currency, goal, country, duration_days):
    df = pd.DataFrame(
        columns=['main_category', 'currency', 'goal', 'country', 
                 'duration_days'], 
        data=[[main_category, currency, goal, country, duration_days]]
    )
    y_pred = pipeline.predict(df)[0]
    if y_pred == 1:
        return html.Img(src='assets/funded_with_kickstarter_badge.png',
        className='img-fluid', style = {'height': '400px'})
    else:
        return html.Img(src='assets/not_funded_with_kickstarter_badge.png',
        className='img-fluid', style = {'height': '400px'})

layout = dbc.Row([column1, column2])