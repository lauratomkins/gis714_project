# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 20:10:31 2020

@author: laura
"""

import pyart
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches


locs = pyart.io.nexrad_common.NEXRAD_LOCATIONS
names = ['KOKX', 'KBOX', 'KDIX', 'KDOX', 'KGYX', 'KENX', 'KBGM']
colors = ['#8dd3c7','#bebada','#ffffb3','#fb8072','#80b1d3','#fdb462','#b3de69']

plt.figure(figsize=(7*1.09,7))
ax = plt.axes(projection=ccrs.PlateCarree()) #make the map axis
ax.add_feature(cfeature.STATES.with_scale('50m'),edgecolor='black',lw=0.5) #add US states
ax.add_feature(cartopy.feature.OCEAN.with_scale('50m'),zorder=0, edgecolor='black',lw=0.25,facecolor=[1,1,1]) #add ocean
ax.add_feature(cartopy.feature.LAND.with_scale('50m'), edgecolor='black',lw=0.25,facecolor='#e0e0e0') #add land with grey face
ax.add_feature(cartopy.feature.LAKES.with_scale('50m'), edgecolor='black',zorder=0, lw=0.25,facecolor=[1,1,1])#add lakes
# plot the radar data
for key in names:
    lon = locs[key]['lon']
    lat = locs[key]['lat']
    ax.tissot(rad_km=200, lons=[lon], lats=[lat], alpha=0.45, facecolor=colors[names.index(key)], edgecolor='black')
    ax.scatter(lon,lat,marker='o',s=60,color='r',zorder=2)
    plt.text(lon+0.2, lat+0.2, key, color='k', fontsize=14)
    
    
#    ax.add_patch(mpatches.Circle(xy=[lon, lat], radius=200,
#                                    facecolor='blue',
#                                    alpha=0.2,
#                                    transform=ccrs.PlateCarree())
#                 )
#set the ticks
ax.set_xticks(np.arange(-80, -68, 2), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(36, 50, 2), crs=ccrs.PlateCarree())
lon_formatter = LongitudeFormatter(zero_direction_label=True)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)  
ax.tick_params(axis='both', labelsize=14)

#set the bounds of the map
ax.set_extent([-79.15, -68.37, 36.01, 46.79])
#Add GMI colorbar
#set title
ax.set_title("Radar locations",fontsize=14, loc='left')
