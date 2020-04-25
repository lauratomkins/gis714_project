# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 15:07:45 2020

@author: laura
"""

import numpy as np
import os
import pandas as pd
import sys
sys.path.append("C:\\Users\\laura\\Documents\\GitHub\\PyART-processing")
import gen_fun
import cv2
from skimage import morphology

tilt = 0.5
names = ['KENX', 'KBUF', 'KBGM', 'KTYX']
date = '20200218'
threshold = -0.1 # From Nicole Hoban

for iradar in names:
    
    print(iradar)
    
    filepath = "G:\\My Drive\\phd\\plotly\\data\\pd\\" + iradar + '\\' + date + '\\'
    
    filelist = gen_fun.get_filelist(filepath, iradar, False)
    
    for ifile in np.arange(len(filelist)-1):
        
        print(ifile)
    
        rad1 = pd.read_pickle(filepath + filelist[ifile]) # read in file
        rad2 = pd.read_pickle(filepath + filelist[ifile+1])
        
        waves = abs(rad2.vel)-abs(rad1.vel)
    
        waves_binary = waves
        waves_binary[waves_binary > threshold] = 0
        waves_binary[waves_binary <= threshold] = 1
        
        wave_blobs = waves_binary.values.reshape((int(np.sqrt(len(waves_binary))), int(np.sqrt(len(waves_binary))))).astype(np.uint8)
        
        retval, labels = cv2.connectedComponents(wave_blobs, connectivity=4)
        
        wave_filtered = morphology.remove_small_objects(labels, min_size=3, connectivity=4)
        wave_filtered[wave_filtered!=0] = 1
        
        rad1_waves = rad1.assign(waves = wave_filtered.flatten())
    
        savepath = "G:\\My Drive\\phd\\plotly\\data\\pd_waves\\" + iradar + '\\' + date + '\\'
        
        if not os.path.exists(savepath):
            os.makedirs(savepath)
        
        rad1_waves.to_pickle(savepath + filelist[ifile])