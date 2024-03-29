import pandas as pd
import dash
import os
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import requests

def some_function():
    from app import wsgi
    # Rest of the function



app = dash.Dash(__name__,title='Analytics Dashboard')
server=app.server
#app._favicon = ("D:/pythonProject/assets/favicon.ico")

######################### From drive excel file read the data

# import pandas as pd
# from openpyxl import load_workbook
# import requests

# # Replace 'YOUR_FILE_ID' with the actual file ID from the shareable link
# file_id = '1PlLImxy_gIg1cf2DLgrhfxqg3Fy2Q2PV'

# # Construct the download link
# download_link = f'https://drive.google.com/uc?id={file_id}'

# # Download the file content using requests
# response = requests.get(download_link)

# # Create a Pandas DataFrame directly from the Excel content
# df = pd.read_excel(pd.ExcelFile(response.content))

# # Now 'df' contains your data, and you can perform operations on it as a DataFrame


########################### FROM CSV ###################################

import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote
from io import StringIO

# Replace 'YOUR_FILE_ID' with the actual file ID from the shareable link
file_id = '1csczi0umdm_paIrW3rc_T01o1wfC2Smv'

# Construct the download link
download_link = f'https://drive.google.com/uc?id={file_id}'

# Download the file content using requests
response = requests.get(download_link)

# Check if the response is an HTML page indicating a warning
if 'Virus scan warning' in response.text:
    soup = BeautifulSoup(response.text, 'html.parser')
    download_link = soup.find('form', {'id': 'download-form'}).get('action')
    response = requests.get(download_link, params={'id': file_id, 'confirm': 't'})

# Create a Pandas DataFrame directly from the CSV content
csv_content = response.text
df = pd.read_csv(StringIO(csv_content))

#############################################################################################################




#df=pd.read_csv("df_new123.csv")
#print(df.Location.unique())


app.layout=html.Div([
    html.Img(src='/assets/image.png',height=75,width=300),
    html.H1("Analytics dashboard for sensor based network in west bengal",style={'textAlign': 'center'}),
    dcc.Dropdown(id='Location-choice',
                 options=[{'label':x, 'value':x}
                          for x in sorted(df.Location.unique())],
                 value='A.B.N. Seal College'
                 ),

    #dcc.Graph(id='my_graph',figure={}),
html.Div(children=[
        dcc.Graph(id="graph1", style={'display': 'flex'},figure={}),
        #dcc.Graph(id="graph2", style={'display': 'inline-block'},figure={})
        dcc.Graph(id="graph2", style={'display': 'flex'},figure={})
    ]),


html.Div([
        html.H1("Sensor Location",style={'textAlign': 'center','backgroundColor':'lightblue'}),
        html.Iframe(id='map1',srcDoc=open('map.html','r').read(),width='400',height='600')
    ])


])


@app.callback(
    [Output(component_id='graph1',component_property='figure'),
     Output(component_id='graph2',component_property='figure')],
    Input(component_id='Location-choice',component_property='value')
)

def interactive_dashboard(value_Location):
    #print(value_Location)
    df1=df[df.Location==value_Location]
    #fig=px.scatter(data_frame=df1,x='Date', y='PM 2.5 AVG (µg/m³)',hover_data=['Hour'], range_color=[0,150])
    fig1 = px.scatter(df1, x='Date', y='Hour', color='PM 2.5 AVG (µg/m³)',hover_data=['Hour'], range_color=[0,120])
    fig2 = px.scatter(df1, x='Date', y='Hour', color='PM 10 AVG (µg/m³)', hover_data=['Hour'], range_color=[0,200])

    return fig1,fig2


if __name__=='__main__':
    app.run_server(debug=True)


