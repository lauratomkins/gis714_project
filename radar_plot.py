# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 11:09:20 2020

@author: laura
"""

import numpy as np
import pandas as pd
import sys
#sys.path.append("C:\\Users\\laura\\Documents\\GitHub\\PyART-processing")
#sys.path.append("C:\\Users\\laura\\Documents\\GitHub\\gis714_project\\")
sys.path.append("C:\\Users\\lmtomkin\\Documents\\winter_storms\\PyART-processing") # work computer
sys.path.append("C:\\Users\\lmtomkin\\Documents\\GitHub\\gis714_project\\")
import gen_fun
from datetime import datetime
import os
import plotter

# Define plot radars, center radar, and date
names = ['KENX', 'KBUF', 'KBGM', 'KTYX']
center = names[3]
date = '20200218'
center_lon = -75.6791; center_lat = 43.7558; center_alt = 567.4;

#GDrive = "G:\\My Drive\\" # personal computer
GDrive = "Q:\\My Drive\\" # personal computer

# Set plotting flags and muting threshold
plot_ref = True; plot_rho = True; plot_vel = True; plot_waves = True;
mute_ref = True
mute_thres = 0.9

# Set center radar paths, list, and dates
center_path = GDrive + "\\phd\\plotly\\data\\pd_interp_waves\\" + center + '\\' + date + '\\'
center_list = gen_fun.get_filelist(center_path, center, False)
center_date = [datetime.strptime(date + i[13:19], "%Y%m%d%H%M%S") for i in center_list] # extract dates from filename

# Remove center radar from list to iterate
names.remove(center)
filelists = {} # define empty dict to store filelists
remain_dates = {} # define empty dict to store times

# loop through non-center radar to get list of dates
for iremain in names:
    
    filepath = GDrive + "\\phd\\plotly\\data\\pd_interp_waves\\" + iremain + '\\' + date + '\\'
    filelist = gen_fun.get_filelist(filepath, iremain, False)    
    filelists[iremain] = filelist # populate dictionary with filepaths
    filedate = [datetime.strptime(date + i[13:19], "%Y%m%d%H%M%S") for i in filelist]
    remain_dates[iremain] = filedate # populate dictionary with list of dates

# Loop through all center times for stitching and plotting
for itime in np.arange(len(center_date)):
    
    print(itime)
    
    fullpaths = []
    fullpaths.append(center_path + center_list[itime])
    
    # Loop through remaining radars to find closest file with time match
    for iradar in names:
        
        time_diff = [abs(center_date[itime] - idate) for idate in remain_dates[iradar]]
        min_idx = time_diff.index(min(time_diff))
        
        filepath = GDrive + "\\phd\\plotly\\data\\pd_interp_waves\\" + iradar + '\\' + date + '\\'
        fullpaths.append(filepath + filelists[iradar][min_idx]) # full path of matching time
        
    # concatenate each into large pandas array    
    large_pd = pd.read_pickle(fullpaths[0])
    
    for path in fullpaths[1:]:
        
        large_pd = pd.concat([large_pd, pd.read_pickle(path)]).groupby(['lat','lon']).agg({'ref':'max','rho':'max','vel':'mean','waves':'max'}) # concatenate into large pandas df
        large_pd = large_pd.reset_index() 
    
    large_pd.columns = ['lat', 'lon', 'ref_max', 'rho_max', 'vel_mean', 'waves_max']
    filtered = large_pd.dropna(axis=0, how='all', subset=['ref_max', 'rho_max', 'vel_mean']) # if all values are NaN then remove that row
    
    #filtered.loc[(filtered['rho_max'] < mute_thres) & (filtered['rho_max'] != 0) & (filtered['ref_max'] != 0), 'ref_max'] = np.nan

    pklpath = GDrive + "\\phd\\plotly\\data\\pd_stitched\\" + iradar + '\\' + date + '\\'
        
    if not os.path.exists(pklpath):
        os.makedirs(pklpath)
        
    filtered.to_pickle(pklpath + center_list[itime])
    
    image_path = GDrive + "\\phd\\plotly\\images\\"
    
    plotter.ref_plot(filtered, center_date[itime], 'ref', image_path, mute_ref, mute_thres)
    plotter.ref_plot(filtered, center_date[itime], 'ref', image_path, False, 'N/A')
    plotter.rho_plot(filtered, center_date[itime], 'rho', image_path)
    plotter.vel_plot(filtered, center_date[itime], 'vel', image_path)
    plotter.waves_plot(filtered, center_date[itime], 'waves', image_path)
#    plt.figure(figsize=(9,9*1.91))
#    ax = plt.axes(projection=ccrs.PlateCarree()) #make the map axis
#    ax.add_feature(cfeature.STATES.with_scale('50m'),edgecolor='black',lw=0.25) #add US states
#    ax.add_feature(cartopy.feature.OCEAN.with_scale('50m'),zorder=0, edgecolor='black',lw=0.25,facecolor=[1,1,1]) #add ocean
#    ax.add_feature(cartopy.feature.LAND.with_scale('50m'), edgecolor='black',lw=0.25,facecolor='#e0e0e0') #add land with grey face
#    ax.add_feature(cartopy.feature.LAKES.with_scale('50m'), edgecolor='black',zorder=0, lw=0.25,facecolor=[1,1,1])#add lakes
#    #plot the DPR swath 
#    pm2 = ax.scatter(filtered.lon[filtered.ref_max!=0], filtered.lat[filtered.ref_max!=0], c=filtered.ref_max[filtered.ref_max!=0],s=0.5,vmin=0,vmax=40,cmap="magma_r")
#    pmnan = ax.scatter(filtered[filtered['ref_max'].isnull()].lon, filtered[filtered['ref_max'].isnull()].lat, c='#666666', s=0.5)
#    #set the ticks
#    ax.set_xticks(np.arange(-84, -68, 2), crs=ccrs.PlateCarree())
#    ax.set_yticks(np.arange(38, 46, 2), crs=ccrs.PlateCarree())
#    lon_formatter = LongitudeFormatter(zero_direction_label=True)
#    lat_formatter = LatitudeFormatter()
#    ax.xaxis.set_major_formatter(lon_formatter)
#    ax.yaxis.set_major_formatter(lat_formatter)  
#    #set the bounds of the map
#    ax.set_extent([-83,-69.5,39,45.5])
#    #Add GMI colorbar
#    cbar = plt.colorbar(pm2,shrink=0.2, extend='max')
#    cbar.set_label('Reflectivity $[dBZ]$',fontsize=14)
#    cbar.ax.tick_params(labelsize=12)
#    #set title
#    ax.set_title(datetime.strftime(center_date[itime], "%d %b %Y %H:%M:%S UTC"),fontsize=14, loc='left')
#    
#    savepath = "G:\\My Drive\\phd\\plotly\\images\\" + date + '\\'
#        
#    if not os.path.exists(savepath):
#        os.makedirs(savepath)
#    
#    plt.savefig(savepath+datetime.strftime(center_date[itime], "%Y%m%d%H%M%S")+'.png',dpi=500,bbox_inches='tight')    
            
    
    
#xpts = 2000*np.arange(-300,301,1); ypts = 2000*np.arange(-300,301,1); zpts = np.zeros([1,601]); # array for interpolation
##center_lon_rad, center_lat_rad = np.deg2rad([center_lon, center_lat]) # convert center lat/lon to radians
#
#[lat_list, lon_list, alt_list] = pm.enu2geodetic(xpts, ypts, zpts, center_lat, center_lon, center_alt)
#[lon_grid, lat_grid] = np.meshgrid(lon_list, lat_list)
#
#ref_grid = griddata((filtered.lon[:100], filtered.lat[:100]), filtered.ref[:100], (lon_grid, lat_grid), method='linear')