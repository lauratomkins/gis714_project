# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 11:49:37 2020

@author: lmtomkin
"""


import pyart
#import matplotlib.pyplot as plt
import numpy as np
#import cartopy.crs as ccrs
import os
os.chdir("C:\\Users\\lmtomkin\\Documents\\Python Scripts")
import radFun
os.chdir("C:\\Users\\lmtomkin\\Documents\\winter_storms\\PyART-processing")
import datashader as ds
import datashader.transfer_functions as tf
import plotly.express as px
import pandas as pd
import matplotlib as mpl
import plotly.io as pio
pio.renderers.default = 'browser'
#import quality_control
#from metpy.io import Level2File

tilt = 0.5

KOKXfile = "C:\\Users\\lmtomkin\\Documents\\winter_storms\\data\\NEXRAD\\KOKX\\20191201\\KOKX20191201_160922_V06"
#KDIXfile = "C:\\Users\\lmtomkin\\Documents\\winter_storms\\data\\NEXRAD\\KDIX\\20191201\\KDIX20191201_160710_V06"

radar = pyart.io.read_nexrad_archive(KOKXfile) # read in file

# find indices of where 0.5 deg tilts are
elevAngles = radar.fixed_angle['data']
elevDiff = elevAngles - tilt
lowTilts = np.where(elevDiff == np.min(elevDiff))[0]

radar = radar.extract_sweeps(lowTilts) # radar object with only 0.5 deg tilts

corr_vel = pyart.correct.dealias_region_based(radar,vel_field="velocity",skip_along_ray=100,skip_between_rays=100,gatefilter=False,keep_original=False)
radar.add_field("dealiased_velocity", corr_vel, True)

radarRange = radar.range['data'][-1]

grid = pyart.map.grid_from_radars(
        radar, 
        grid_shape = (1, 401, 401),
        grid_limits = ((0, 2000), (-radarRange, radarRange), (-radarRange, radarRange)))
#
display = pyart.graph.GridMapDisplay(grid)
display.plot_grid("dealiased_velocity", vmin=-50, vmax=50, cmap='RdBu_r')
display.plot_grid("reflectivity", vmin=-5, vmax=50, cmap='magma_r')
display.plot_grid("cross_correlation_ratio", vmin=0, vmax=1, cmap="bone")


#veltilt, vel = radFun.getDataSweep(radar, 'velocity', tilt)
rhotilt, rho = radFun.getDataSweep(radar, 'cross_correlation_ratio', tilt)
dveltilt, dvel = radFun.getDataSweep(radar, 'dealiased_velocity', tilt)

#ref = radar.fields['reflectivity']['data'][radar.get_slice(rhotilt)]

rho = grid.fields['cross_correlation_ratio']['data'][radar.get_slice(rhotilt)]
ref = grid.fields['reflectivity']['data']
vel = grid.fields['dealiased_velocity']['data']

lat = grid.point_latitude['data']
lon = grid.point_longitude['data']

df = pd.DataFrame({'lat':lat.flatten(), 'lon':lon.flatten(), 'ref':ref.flatten(), 'rho':rho.flatten(), 'vel':vel.flatten()})
df = df.dropna(axis=0, how='all', subset=['ref', 'rho', 'vel'])

cvs = ds.Canvas(plot_width=1000, plot_height=1000)
agg = cvs.points(df, x='lon', y='lat')
coords_lat, coords_lon = agg.coords['lat'].values, agg.coords['lon'].values
coordinates = [[coords_lon[0], coords_lat[0]],
               [coords_lon[-1], coords_lat[0]],
               [coords_lon[-1], coords_lat[-1]],
               [coords_lon[0], coords_lat[-1]]]

img = tf.shade(agg, cmap=mpl.cm.get_cmap('magma_r'))[::-1].to_pil()


fig = px.scatter_mapbox(df, lat='lat', lon='lon', color='ref', color_continuous_scale=px.colors.sequential.Magma_r, zoom=3, range_color=[-5,50])
fig.update_layout(mapbox_style = 'open-street-map',
                  mapbox_layers = [
                          {
                                  "sourcetype": "image",
                                  "source": img,
                                  "coordinates": coordinates}])
fig.show()






