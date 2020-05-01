# GIS714 Project

## List of files used in this project and brief description

`nexrad.py`: Downloads NEXRAD data from AWS. Must specify date and radar.

`nexrad_loc.py`: Plots radars on map.

`radar2pd.py`: Takes radar files, interpolates to a large grid, and converts the to pandas dataframe with latitude, longitude, and the data at each point.

`waves.py`: Calculates waves from output of `radar2pd.py` and saves to a separate pandas dataframe.

`radar_plot.py`: Combines data from multiple radars. Must specify a central radar to match times to.

`plotter.py`: Functions for actually plotting the radar data.
 
