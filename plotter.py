# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 16:28:46 2020

@author: laura
"""
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import cmocean
import matplotlib as mpl

def ref_plot(df, save_date, save_flag, filter_flag, filter_val):
    
    if filter_flag:
        df.loc[(df['rho_max'] < filter_val) & (df['rho_max'] != 0) & (df['ref_max'] != 0), 'ref_max'] = np.nan
        
        save_flag = save_flag + '_' + str(filter_val)
    
    # define figure
    plt.figure(figsize=(9,9*1.91))
    ax = plt.axes(projection=ccrs.PlateCarree()) #make the map axis
    ax.add_feature(cfeature.STATES.with_scale('50m'),edgecolor='black',lw=0.25) #add US states
    ax.add_feature(cartopy.feature.OCEAN.with_scale('50m'),zorder=0, edgecolor='black',lw=0.25,facecolor=[1,1,1]) #add ocean
    ax.add_feature(cartopy.feature.LAND.with_scale('50m'), edgecolor='black',lw=0.25,facecolor='#e0e0e0') #add land with grey face
    ax.add_feature(cartopy.feature.LAKES.with_scale('50m'), edgecolor='black',zorder=0, lw=0.25,facecolor=[1,1,1])#add lakes
    # plot the radar data
    pm2 = ax.scatter(df.lon[df.ref_max!=0], df.lat[df.ref_max!=0], c=df.ref_max[df.ref_max!=0],s=0.5,vmin=0,vmax=40,cmap="magma_r")
    try: 
        ax.scatter(df[df['ref_max'].isnull()].lon, df[df['ref_max'].isnull()].lat, c='#666666', s=0.2)
    except:
        print('No NaN values to mask')
    #set the ticks
    ax.set_xticks(np.arange(-84, -68, 2), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(38, 46, 2), crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)  
    #set the bounds of the map
    ax.set_extent([-83,-69.5,39,45.5])
    #Add GMI colorbar
    cbar = plt.colorbar(pm2,shrink=0.2, extend='max')
    cbar.set_label('Reflectivity $[dBZ]$',fontsize=14)
    cbar.ax.tick_params(labelsize=12)
    #set title
    ax.set_title(datetime.strftime(save_date, "%d %b %Y %H:%M:%S UTC"),fontsize=14, loc='left')
    
    savepath = "G:\\My Drive\\phd\\plotly\\images\\" + datetime.strftime(save_date, "%Y%m%d") + '\\' + save_flag + '\\'
        
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    
    plt.savefig(savepath+datetime.strftime(save_date, "%Y%m%d%H%M%S")+'.png',dpi=500,bbox_inches='tight')    
    
def rho_plot(df, save_date, save_flag):
    
    # define figure
    plt.figure(figsize=(9,9*1.91))
    ax = plt.axes(projection=ccrs.PlateCarree()) #make the map axis
    ax.add_feature(cfeature.STATES.with_scale('50m'),edgecolor='black',lw=0.25) #add US states
    ax.add_feature(cartopy.feature.OCEAN.with_scale('50m'),zorder=0, edgecolor='black',lw=0.25,facecolor=[1,1,1]) #add ocean
    ax.add_feature(cartopy.feature.LAND.with_scale('50m'), edgecolor='black',lw=0.25,facecolor='#e0e0e0') #add land with grey face
    ax.add_feature(cartopy.feature.LAKES.with_scale('50m'), edgecolor='black',zorder=0, lw=0.25,facecolor=[1,1,1])#add lakes
    # plot the radar data
    pm2 = ax.scatter(df.lon[df.rho_max!=0], df.lat[df.rho_max!=0], c=df.rho_max[df.rho_max!=0],s=0.2,vmin=0.6,vmax=1.0,cmap=cmocean.cm.ice_r)
    #set the ticks
    ax.set_xticks(np.arange(-84, -68, 2), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(38, 46, 2), crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)  
    #set the bounds of the map
    ax.set_extent([-83,-69.5,39,45.5])
    #Add GMI colorbar
    cbar = plt.colorbar(pm2,shrink=0.2, extend='both')
    cbar.set_label('rhoHV',fontsize=14)
    cbar.ax.tick_params(labelsize=12)
    #set title
    ax.set_title(datetime.strftime(save_date, "%d %b %Y %H:%M:%S UTC"),fontsize=14, loc='left')
    
    savepath = "G:\\My Drive\\phd\\plotly\\images\\" + datetime.strftime(save_date, "%Y%m%d") + '\\' + save_flag + '\\'
        
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    
    plt.savefig(savepath+datetime.strftime(save_date, "%Y%m%d%H%M%S")+'.png',dpi=500,bbox_inches='tight')    
    
def vel_plot(df, save_date, save_flag):
    
    # define figure
    plt.figure(figsize=(9,9*1.91))
    ax = plt.axes(projection=ccrs.PlateCarree()) #make the map axis
    ax.add_feature(cfeature.STATES.with_scale('50m'),edgecolor='black',lw=0.25) #add US states
    ax.add_feature(cartopy.feature.OCEAN.with_scale('50m'),zorder=0, edgecolor='black',lw=0.25,facecolor=[1,1,1]) #add ocean
    ax.add_feature(cartopy.feature.LAND.with_scale('50m'), edgecolor='black',lw=0.25,facecolor='#e0e0e0') #add land with grey face
    ax.add_feature(cartopy.feature.LAKES.with_scale('50m'), edgecolor='black',zorder=0, lw=0.25,facecolor=[1,1,1])#add lakes
    # plot the radar data
    pm2 = ax.scatter(df.lon[df.vel_mean!=0], df.lat[df.vel_mean!=0], c=df.vel_mean[df.vel_mean!=0],s=0.2,vmin=-15,vmax=15,cmap='RdBu_r')
    #set the ticks
    ax.set_xticks(np.arange(-84, -68, 2), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(38, 46, 2), crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)  
    #set the bounds of the map
    ax.set_extent([-83,-69.5,39,45.5])
    #Add GMI colorbar
    cbar = plt.colorbar(pm2,shrink=0.2, extend='both')
    cbar.set_label('Velocity $[ms^{-1}]$',fontsize=14)
    cbar.ax.tick_params(labelsize=12)
    #set title
    ax.set_title(datetime.strftime(save_date, "%d %b %Y %H:%M:%S UTC"),fontsize=14, loc='left')
    
    savepath = "G:\\My Drive\\phd\\plotly\\images\\" + datetime.strftime(save_date, "%Y%m%d") + '\\' + save_flag + '\\'
        
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    
    plt.savefig(savepath+datetime.strftime(save_date, "%Y%m%d%H%M%S")+'.png',dpi=500,bbox_inches='tight')    


def waves_plot(df, save_date, save_flag):
    
    #df.loc[(df['waves_mean'] >= 0.5), 'waves_mean'] = 1
    #df.loc[(df['waves_mean'] < 0.5), 'waves_mean'] = 0
    
    # define figure
    plt.figure(figsize=(9,9*1.91))
    ax = plt.axes(projection=ccrs.PlateCarree()) #make the map axis
    ax.add_feature(cfeature.STATES.with_scale('50m'),edgecolor='black',lw=0.25) #add US states
    ax.add_feature(cartopy.feature.OCEAN.with_scale('50m'),zorder=0, edgecolor='black',lw=0.25,facecolor=[1,1,1]) #add ocean
    ax.add_feature(cartopy.feature.LAND.with_scale('50m'), edgecolor='black',lw=0.25,facecolor='#e0e0e0') #add land with grey face
    ax.add_feature(cartopy.feature.LAKES.with_scale('50m'), edgecolor='black',zorder=0, lw=0.25,facecolor=[1,1,1])#add lakes
    # plot the radar data
    ax.scatter(df.lon[df.waves_max!=0], df.lat[df.waves_max!=0], c='black',s=0.2)
    #set the ticks
    ax.set_xticks(np.arange(-84, -68, 2), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(38, 46, 2), crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)  
    #set the bounds of the map
    ax.set_extent([-83,-69.5,39,45.5])
    #set title
    ax.set_title(datetime.strftime(save_date, "%d %b %Y %H:%M:%S UTC"),fontsize=14, loc='left')
    
    savepath = "G:\\My Drive\\phd\\plotly\\images\\" + datetime.strftime(save_date, "%Y%m%d") + '\\' + save_flag + '\\'
        
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    
    plt.savefig(savepath+datetime.strftime(save_date, "%Y%m%d%H%M%S")+'.png',dpi=500,bbox_inches='tight')    
