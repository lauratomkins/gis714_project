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
sys.path.append("C:\\Users\\laura\\Documents\\GitHub\\PyART-processing")
import gen_fun

tilt = 0.5
names = ['KENX', 'KBUF', 'KBGM', 'KTYX']
date = '20200218'

for iradar in names:
    
    filepath = "G:\\My Drive\\phd\\plotly\\data\\NEXRAD\\" + iradar + '\\' + date + '\\'
    
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
    
        df = pd.DataFrame({'lat':lat.flatten(), 'lon':lon.flatten(), 'ref':ref.flatten(), 'rho':rho.flatten(), 'vel':vel.flatten()})
        #df = df.dropna(axis=0, how='all', subset=['ref', 'rho', 'vel'])
        
        savepath = "G:\\My Drive\\phd\\plotly\\data\\pd\\" + iradar + '\\' + date + '\\'
        
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        
        df.to_pickle(savepath + ifile + '.pkl')