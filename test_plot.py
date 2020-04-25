# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 12:29:15 2020

@author: laura
"""

import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.patheffects as PathEffects
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt

waves_binary[waves_binary==0] = np.nan

#define figure
plt.figure(figsize=(12,12))
#make the map axis
ax = plt.axes(projection=ccrs.PlateCarree())
#add US states
ax.add_feature(cfeature.STATES.with_scale('50m'),lw=0.5)
#add ocean
ax.add_feature(cartopy.feature.OCEAN.with_scale('50m'))
#add land with grey face
ax.add_feature(cartopy.feature.LAND.with_scale('50m'), edgecolor='black',lw=0.5,facecolor=[0.95,0.95,0.95])

#plot GMI data only outside the GPM-DPR swath, this is a bit of hard coding with the 92/137
pm = ax.scatter(rad1.lon,rad1.lat,c=waves_binary,s=0.5,edgecolor=None,zorder=3,alpha=0.75,vmin=0,vmax=1)

#add GMI colorbar
cbar = plt.colorbar(pm,shrink=0.3)
cbar.ax.tick_params(labelsize=12)

#Add DPR colorbar
cbar = plt.colorbar(pm2,shrink=0.3)
cbar.set_label('Z, [dBZ]',fontsize=14)
cbar.ax.tick_params(labelsize=12)

#set title
ax.set_title('GPM CO Overpass, 1035 UTC',fontsize=14)

plt.tight_layout()