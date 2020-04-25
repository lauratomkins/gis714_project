# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 11:09:20 2020

@author: laura
"""

import numpy as np
import pandas as pd
import sys
sys.path.append("C:\\Users\\laura\\Documents\\GitHub\\PyART-processing")
import gen_fun
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import pymap3d as pm
from scipy.interpolate import griddata

# Define plot radars, center radar, and date
names = ['KENX', 'KBUF', 'KBGM', 'KTYX']
center = names[3]
date = '20200218'
center_lon = -75.6791; center_lat = 43.7558; center_alt = 567.4;

# Set plotting flags and muting threshold
plot_ref = True; plot_rho = True; plot_vel = True; plot_waves = True;
mute_ref = True
mute_thres = 0.9

# Set center radar paths, list, and dates
center_path = "G:\\My Drive\\phd\\plotly\\data\\pd_waves\\" + center + '\\' + date + '\\'
center_list = gen_fun.get_filelist(center_path, center, False)
center_date = [datetime.strptime(date + i[13:19], "%Y%m%d%H%M%S") for i in center_list] # extract dates from filename

# Remove center radar from list to iterate
names.remove(center)
filelists = {} # define empty dict to store filelists
remain_dates = {} # define empty dict to store times

# loop through non-center radar to get list of dates
for iremain in names:
    
    filepath = "G:\\My Drive\\phd\\plotly\\data\\pd_waves\\" + iremain + '\\' + date + '\\'
    filelist = gen_fun.get_filelist(filepath, iremain, False)    
    filelists[iremain] = filelist # populate dictionary with filepaths
    filedate = [datetime.strptime(date + i[13:19], "%Y%m%d%H%M%S") for i in filelist]
    remain_dates[iremain] = filedate # populate dictionary with list of dates

# Loop through all center times for stitching and plotting
for itime in np.arange(len(center_date)):
    
    fullpaths = []
    fullpaths.append(center_path + center_list[itime])
    
    # Loop through remaining radars to find closest file with time match
    for iradar in names:
        
        time_diff = [abs(center_date[itime] - idate) for idate in remain_dates[iradar]]
        min_idx, min_diff = min(enumerate(time_diff))
        
        filepath = "G:\\My Drive\\phd\\plotly\\data\\pd_waves\\" + iradar + '\\' + date + '\\'
        fullpaths.append(filepath + filelists[iradar][min_idx]) # full path of matching time
        
    # concatenate each into large pandas array    
    large_pd = pd.read_pickle(fullpaths[0])
    
    for path in fullpaths[1:]:
        
        large_pd = pd.concat([large_pd, pd.read_pickle(path)]) # concatenate into large pandas df
        
    filtered = large_pd.dropna(axis=0, how='all', subset=['ref', 'rho', 'vel']) # if all values are NaN then remove that row
    
    xpts = 2000*np.arange(-300,301,1); ypts = 2000*np.arange(-300,301,1); zpts = np.zeros([1,601]); # array for interpolation
    #center_lon_rad, center_lat_rad = np.deg2rad([center_lon, center_lat]) # convert center lat/lon to radians
    
    [lat_list, lon_list, alt_list] = pm.enu2geodetic(xpts, ypts, zpts, center_lat, center_lon, center_alt)
    [lon_grid, lat_grid] = np.meshgrid(lon_list, lat_list)
    
    ref_grid = griddata((filtered.lon[:100], filtered.lat[:100]), filtered.ref[:100], (lon_grid, lat_grid), method='linear')


    plt.figure(figsize=(9,9*1.91))
    ax = plt.axes(projection=ccrs.PlateCarree()) #make the map axis
    ax.add_feature(cfeature.STATES.with_scale('50m'),lw=0.5) #add US states
    ax.add_feature(cartopy.feature.OCEAN.with_scale('50m')) #add ocean
    ax.add_feature(cartopy.feature.LAND.with_scale('50m'), edgecolor='black',lw=0.5,facecolor=[0.95,0.95,0.95]) #add land with grey face
    #ax.add_feature(cartopy.feature.LAKES.with_scale('50m'), edgecolor='black')#add lakes
    #plot the DPR swath 
    #pm2 = ax.pcolormesh(filtered.lon[::-1], filtered.lat[::-1], filtered.ref[::-1],alpha=0.7,vmin=0,vmax=40,cmap="magma_r", interpolation='nearest')
    pm2 = ax.pcolormesh(lon_grid, lat_grid,ref_grid,alpha=0.7,vmin=0,vmax=40,cmap="magma_r")#,edgecolor='k',linewidth=0.001)
    #set the ticks
    ax.set_xticks(np.arange(-84, -68, 2), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(38, 46, 2), crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)  
    #set the bounds of the map
    ax.set_extent([-83,-69,39,46])
    #Add GMI colorbar
    cbar = plt.colorbar(pm2,shrink=0.2, extend='both')
    cbar.set_label('Reflectivity $[dBZ]$',fontsize=14)
    cbar.ax.tick_params(labelsize=12)
    #set title
    ax.set_title('GPM GMI Overpass, 20200118 1900 UTC',fontsize=14)
    
    plt.savefig(image_folder+'20200118_GPM_GMI_rr.png',dpi=500,bbox_inches='tight')    
            