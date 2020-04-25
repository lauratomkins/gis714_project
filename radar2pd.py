# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 15:07:45 2020

@author: laura
"""

import pyart
import numpy as np
import os
import pandas as pd
import sys
#sys.path.append("C:\\Users\\laura\\Documents\\GitHub\\PyART-processing") # personal computer
sys.path.append("C:\\Users\\lmtomkin\\Documents\\winter_storms\\PyART-processing") # work computer
import gen_fun
import pymap3d as pm
from scipy.interpolate import griddata

tilt = 0.5
names = ['KENX', 'KBUF', 'KBGM', 'KTYX']
date = '20200218'
center = names[3]
date = '20200218'
center_lon = -75.6791; center_lat = 43.7558; center_alt = 567.4;

for iradar in names:
    
    #filepath = "G:\\My Drive\\phd\\plotly\\data\\NEXRAD\\" + iradar + '\\' + date + '\\' # personal computer
    filepath = "Q:\\My Drive\\phd\\plotly\\data\\NEXRAD\\" + iradar + '\\' + date + '\\' # work computer
    
    filelist = gen_fun.get_filelist(filepath, iradar, False)
    
    for ifile in filelist:
        
        print(ifile)
    
        radar = pyart.io.read_nexrad_archive(filepath + ifile) # read in file
    
        # find indices of where 0.5 deg tilts are
        elevAngles = radar.fixed_angle['data']
        elevDiff = elevAngles - tilt
        lowTilts = np.where(elevDiff == np.min(elevDiff))[0]
    
        radar = radar.extract_sweeps(lowTilts) # radar object with only 0.5 deg tilts
        
        # dealias velocity and add to radar object
        corr_vel = pyart.correct.dealias_region_based(radar,vel_field="velocity",skip_along_ray=100,skip_between_rays=100,gatefilter=False,keep_original=False)
        radar.add_field("dealiased_velocity", corr_vel, True)
        
        # polar to cartesian
        radarRange = radar.range['data'][-1]
    
        grid = pyart.map.grid_from_radars(
                radar, 
                grid_shape = (1, 401, 401),
                grid_limits = ((0, 2000), (-radarRange, radarRange), (-radarRange, radarRange)))
        
        # fields
        rho = grid.fields['cross_correlation_ratio']['data']
        ref = grid.fields['reflectivity']['data']
        vel = grid.fields['dealiased_velocity']['data']
    
        lat = grid.point_latitude['data']
        lon = grid.point_longitude['data']
        
        xpts = 2000*np.arange(-400,401,1); ypts = 2000*np.arange(-400,401,1); zpts = np.zeros([1,801]); # array for interpolation
        #center_lon_rad, center_lat_rad = np.deg2rad([center_lon, center_lat]) # convert center lat/lon to radians
        
        [lat_list, lon_list, alt_list] = pm.enu2geodetic(xpts, ypts, zpts, center_lat, center_lon, center_alt)
        [lon_grid, lat_grid] = np.meshgrid(lon_list, lat_list)
        
        rho_grid = griddata((lon.flatten(), lat.flatten()), rho.flatten(), (lon_grid, lat_grid), method='linear')
        ref_grid = griddata((lon.flatten(), lat.flatten()), ref.flatten(), (lon_grid, lat_grid), method='linear')
        vel_grid = griddata((lon.flatten(), lat.flatten()), vel.flatten(), (lon_grid, lat_grid), method='linear')
    
        df = pd.DataFrame({'lat':lat_grid.flatten(), 'lon':lon_grid.flatten(), 'ref':ref_grid.flatten(), 'rho':rho_grid.flatten(), 'vel':vel_grid.flatten()})
        #df = df.dropna(axis=0, how='all', subset=['ref', 'rho', 'vel'])
        
        #savepath = "G:\\My Drive\\phd\\plotly\\data\\pd_interp\\" + iradar + '\\' + date + '\\' # personal computer
        savepath = "Q:\\My Drive\\phd\\plotly\\data\\pd_interp\\" + iradar + '\\' + date + '\\' # work computer
        
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        
        df.to_pickle(savepath + ifile + '.pkl')