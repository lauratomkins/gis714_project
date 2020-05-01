# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 13:53:15 2020

@author: lmtomkin
"""


import pyart
import numpy as np



def getDataSweep(radar, field, tilt):
    
    elevAngles = radar.fixed_angle['data']
    elevDiff = elevAngles - tilt
    lowTilts = np.where(elevDiff == np.min(elevDiff))[0]

    for itilt in np.arange(len(lowTilts)):
        
        tiltSlice = radar.get_slice(lowTilts[itilt])

        data = radar.fields[field]['data'][tiltSlice] 
        
        if ~data.mask.all():     # if NOT all data is masked, exit, if all data is masked continue        
            break
        
    return itilt, data