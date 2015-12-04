import pandas as pd
from pandas import MultiIndex
import numpy as np

import re as regex
import time
import datetime
import random

import math
import distance

# load a test csv
raw_parsed = pd.read_csv('temp4.csv')
raw_parsed = raw_parsed.reset_index(drop=True)

print (len(raw_parsed))

# Edit column names
raw_parsed.columns = ['device_id','time','stamp','current_lat','current_lon','stop_id','fav']


'''==================='''
''' ADD STOP LOCATION '''
'''==================='''


# match bus stop locations
stop_list = pd.read_csv('stops/stop_dict.csv')

stop_list_1 = stop_list[stop_list['agency_id'] == 38] # for logs before March15th, temp4[39571]
stop_list_2 = stop_list[stop_list['agency_id'] == 46] # for logs after March15th

# parse_wStop = pd.merge(raw_parsed, stop_list_2, on='stop_id', how='left')

# for temp4
merged_1 = pd.merge(raw_parsed[:39571], stop_list_1, on='stop_id', how='left')
merged_2 = pd.merge(raw_parsed[39571:], stop_list_2, on='stop_id', how='left')
parse_wStop = pd.concat([merged_1, merged_2], axis=0, ignore_index=True)


# calculate current_lat/lon to stop_lat/lon distances
parse_wStop['distance'] = ''

for i in range(len(parse_wStop)):
    if parse_wStop['stop_lat'][i]:
        lat_now = parse_wStop['current_lat'][i]
        lon_now = parse_wStop['current_lon'][i]
        lat_origin = parse_wStop['stop_lat'][i]
        lon_origin = parse_wStop['stop_lon'][i]
        parse_wStop.loc[i,'distance'] = np.float64(getDistanceFromLatLonInKm(lat_now,lon_now,lat_origin,lon_origin))
    else:
        parse_wStop.loc[i,'distance'] = ''
        

print (len(parse_wStop))

parse_wStop.to_csv('temp4_wStop.csv', index=False)
