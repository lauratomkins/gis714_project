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

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Boostrap CSS for styling.
#app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

df = pd.read_pickle('G://My Drive//phd//plotly//data//pd//KTYX//20200218//KTYX20200218_050127_V06.pkl')
df = df.dropna(axis=0, how='all', subset=['ref', 'rho', 'vel']) # if all values are NaN then remove that row
df['marker_size'] = 0.01

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
    #title="Reflectivity [dBZ]",
    range_color=[0,40])
#fig.update_traces(marker_size=0.5)
fig.update_layout(
    autosize=True,
    height=800,
    margin=dict(
        l=35, r=35, b=35, t=15),
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
    color_continuous_scale=px.colors.sequential.ice[::-1], 
    zoom=4, 
    opacity=0.8,
    #title="rhoHV",
    range_color=[0.7,1])
fig2.update_layout(
    autosize=True,
    height=800,
    margin=dict(
        l=35, r=35, b=35, t=15),
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
app.title = 'Radar Test'
app.layout = html.Div([
    html.Div([
        html.Div([html.Label(["Use slider to mute reflectivity"]),dcc.Slider(
                    id="threshold-slider",
                    min=0.5,
                    max=1,
                    step=0.01,
                    value=0,
                    marks={
                        i: '{:1.2f}'.format(i) for i in np.arange(0.5,1.05,0.05)
                    },
                    )], style={'padding':10,'backgroundColor':'transparent'},className = "six columns"),
        html.Div([html.Label(["Select variable"]),dcc.Dropdown(
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
            [Input('variable-checklist', 'value')])
def update_graph(value):
    df = pd.read_pickle('G://My Drive//phd//plotly//data//pd//KTYX//20200218//KTYX20200218_050127_V06.pkl')
    df = df.dropna(axis=0, how='all', subset=['ref', 'rho', 'vel']) # if all values are NaN then remove that row

    if value == 'rho':
        rng = [0.7,1]
        cb = px.colors.sequential.ice[::-1]
        title_label='rhoHV'

    elif value == 'vel':
        rng = [-30, 30]
        cb = px.colors.sequential.RdBu[::-1]
        title_label="Velocity [m/s]"

    fig = px.scatter_mapbox(
        df, 
        lat='lat', 
        lon='lon', 
        color=value, 
        color_continuous_scale=cb, 
        zoom=4, 
        opacity=0.8,
        #title=title_label,
        range_color=rng)
    fig.update_layout(
        autosize=True,
        height=800,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=15
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
            [Input('threshold-slider', 'value')])
def update_graph2(value):
    df = pd.read_pickle('G://My Drive//phd//plotly//data//pd//KTYX//20200218//KTYX20200218_050127_V06.pkl')
    df = df.dropna(axis=0, how='all', subset=['ref', 'rho', 'vel']) # if all values are NaN then remove that row

    temp = df
    temp.loc[df['rho'] < value, 'ref'] = np.nan

    fig = px.scatter_mapbox(
        temp, 
        lat='lat', 
        lon='lon', 
        color='ref', 
        color_continuous_scale=px.colors.sequential.Magma[::-1], 
        zoom=4, 
        opacity=0.8,
        #title="Reflectivity [dBZ]",
        range_color=[0,40])
    #fig.update_traces(marker_size=0.5)
    fig.update_layout(
        autosize=True,
        height=800,
        margin=dict(
            l=35,
            r=35,
            b=35,
            t=15
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