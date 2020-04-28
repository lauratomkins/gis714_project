# step3_map.py
# GIS 715 Student-led lab - Dash
# Add map of California fires by cause.

# Now we will add a second component to the Dash layout. We can use the scattermapbox plotly object to create a map of fire point locations.
# For now the map is not interactive (beyond the out of the box functionality).
# We will use a style sheet (CSS) to place the components within the layout into rows and columns.

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import numpy as np
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Boostrap CSS for styling.
#app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

filepath = 'G://My Drive//phd//plotly//data//pd_waves//KTYX//20200218//'
filelist = os.listdir(filepath)

df = pd.read_pickle(filepath + filelist[0])
df = df.dropna(axis=0, how='all', subset=['ref', 'rho', 'vel']) # if all values are NaN then remove that row

# Mapbox API key
# Insert your key below.
mapbox_access_token = 'pk.eyJ1Ijoia2VsbHlubSIsImEiOiJjanM0eDF0ZngwMjZ0M3lwYjV5MWxqZm1xIn0.49GaijkpupewHcHf2niUDA'

fig = px.scatter_mapbox(
    df, 
    lat='lat', 
    lon='lon', 
    color='ref', 
    color_continuous_scale=px.colors.sequential.Magma[::-1], 
    zoom=4, 
    opacity=0.8,
    range_color=[0,40])
#fig.update_traces(marker_size=0.5)
fig.update_layout(
    title="Reflectivity [dBZ]",
    autosize=True,
    height=800,
    margin=dict(
        l=35, r=35, b=35, t=25),
    hovermode="closest",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center = dict(
            lon=-75.6791,
            lat=43.7558),
        zoom=6)
    )

fig2 = px.scatter_mapbox(
    df, 
    lat='lat', 
    lon='lon', 
    color='rho', 
    color_continuous_scale=px.colors.sequential.deep, 
    zoom=4, 
    opacity=0.8,
    #title="rhoHV",
    range_color=[0.8,1])
fig2.update_layout(
    title='rhoHV',
    autosize=True,
    height=800,
    margin=dict(
        l=35, r=35, b=35, t=25),
    hovermode="closest",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center = dict(
            lon=-75.6791,
            lat=43.7558),
        zoom=6)
    )


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Radar Image Muting'
app.layout = html.Div([
    html.H1(children='Radar Image Muting'),
    html.H2(children='GIS715 Class Project, Spring 2020'),
    html.Div([
        html.Div([html.Label(["Select file"]),dcc.Dropdown(
                    id="file-selector",
                    options=[
                        {'label': i, 'value': i} for i in filelist
                    ],
                    value = filelist[0]
                    )], style={'padding':10,'backgroundColor':'transparent'},className = "six columns"),
    ],  style={'padding':10},className = "row"),
    html.Div([
        html.Div([html.Label(["Select rhoHV threshold to 'mute' reflectivity"]),dcc.Slider(
                    id="threshold-slider",
                    min=0.5,
                    max=1,
                    step=0.01,
                    value=0,
                    marks={
                        i: '{:1.2f}'.format(i) for i in np.arange(0.5,1.05,0.05)
                    },
                    )], style={'padding':10,'backgroundColor':'transparent'},className = "six columns"),
        html.Div([html.Label(["Select secondary variable to plot"]),dcc.Dropdown(
                    id='variable-checklist',
                    options=[
                        {'label': 'Correlation Coefficient', 'value': 'rho'},
                        {'label': 'Waves', 'value': 'waves'},
                        {'label': 'Velocity', 'value': 'vel'}
                    ],
                    value= 'rho',
                    )],style={'padding':10,'backgroundColor':'transparent'},className = "six columns"),    
    ],  style={'padding':10},className = "row"),
    html.Div([
        html.Div(dcc.Graph(id = "ref_map", figure=fig), style={'padding':10},className = "six columns"),
        html.Div(dcc.Graph(id = "rho-vel_map", figure=fig2), style={'padding': 10},className = "six columns")
    ], style={'padding':10},className = 'row')    
])

@app.callback(Output('rho-vel_map', "figure"),
            [Input('variable-checklist', 'value'),
            Input('file-selector', 'value')])
def update_graph(variable_value, file_value):
    df = pd.read_pickle(filepath + file_value)
    df = df.dropna(axis=0, how='all', subset=['ref', 'rho', 'vel']) # if all values are NaN then remove that row

    if variable_value == 'rho':
        rng = [0.8,1]
        cb = px.colors.sequential.deep
        title_label='rhoHV'

    elif variable_value == 'waves':
        df = df[df['waves']==1]
        cb = px.colors.sequential.gray[::-1]
        rng = [0,1]
        title_label = 'Waves'

    elif variable_value == 'vel':
        rng = [-30, 30]
        cb = px.colors.sequential.RdBu[::-1]
        title_label="Velocity [m/s]"

    fig = px.scatter_mapbox(
        df, 
        lat='lat', 
        lon='lon', 
        color=variable_value, 
        color_continuous_scale=cb, 
        zoom=4, 
        opacity=0.8,
        range_color=rng)
    fig.update_layout(
        title=title_label,
        autosize=True,
        height=800,
        margin=dict(
            l=35, r=35, b=35, t=25
            ),
        hovermode="closest",
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style="light",
            center = dict(
                lon=-75.6791,
                lat=43.7558
            ),
            zoom=6)
        )
    return fig

@app.callback(Output('ref_map', "figure"),
            [Input('threshold-slider', 'value'),
            Input('file-selector', 'value')])
def update_graph2(threshold_value, file_value):
    df = pd.read_pickle(filepath + file_value)
    df = df.dropna(axis=0, how='all', subset=['ref', 'rho', 'vel']) # if all values are NaN then remove that row

    temp = df
    temp.loc[df['rho'] < threshold_value, 'ref'] = np.nan

    fig = px.scatter_mapbox(
        temp, 
        lat='lat', 
        lon='lon', 
        color='ref', 
        color_continuous_scale=px.colors.sequential.Magma[::-1], 
        zoom=4, 
        opacity=0.8,
        range_color=[0,40])
    #fig.update_traces(marker_size=0.5)
    fig.update_layout(
        title="Reflectivity [dBZ]",
        autosize=True,
        height=800,
        margin=dict(
            l=35, r=35,b=35,t=25
            ),
        hovermode="closest",
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style="light",
            center = dict(
                lon=-75.6791,
                lat=43.7558
            ),
            zoom=6)
        )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)