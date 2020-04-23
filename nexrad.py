# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 16:03:52 2019

@author: lmtomkin
"""

import nexradaws
import os

date = '20200218'
radar = 'KBUF'

conn = nexradaws.NexradAwsInterface()

availscans = conn.get_avail_scans(date[0:4], date[4:6], date[6:8], radar)

if not os.path.exists('G:\\My Drive\\phd\\plotly\\data\\NEXRAD\\'+radar+'\\'+date):
    os.makedirs('G:\\My Drive\\phd\\plotly\\data\\NEXRAD\\'+radar+'\\'+date)

results = conn.download(availscans, 'G:\\My Drive\\phd\\plotly\\data\\NEXRAD\\'+radar+'\\'+date)
