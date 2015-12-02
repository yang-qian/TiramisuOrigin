import pandas as pd
from pandas import MultiIndex
import numpy as np

import re as regex
import time
import datetime
import random

import math
import parseTime as pt

stops = pd.read_csv('stop_dict.csv')

'''=================='''
''' Cleansing Traces '''
'''=================='''

# call log format:
# device_id, time, stamp (13digitUNIX), date, tod, numToD, dow, weekday,
# current_lat, currentl_lon, 
# fav,
# stop_id, stop_location, agency_id, route_list, route_cnt, stop_lat, stop_lon,
# distance, timeDif,

raw_trace = pd.read_csv('01_trace2014.csv',
                        usecols = ['device_id','stamp',
                                   'current_lat','current_lon',
                                   'trip_id','origin_id','origin_lat','origin_lon',
                                   'route_short_name','source','agency_id'],
                        parse_dates=True)

raw_trace = raw_trace[raw_trace['source'] == 'recording']

raw_trace = raw_trace.rename(columns = {'route_short_name':'route_id'})

raw_trace = raw_trace.rename(columns = {'origin_id':'stop_id'})
raw_trace = pd.merge(raw_trace, stops, on=['stop_id','agency_id'], how='left')


# Parse UNIX to readable cols
raw_trace['time'] = pd.Series(index=raw_trace.index)
raw_trace['date'] = pd.Series(index=raw_trace.index)
raw_trace['tod'] = pd.Series(index=raw_trace.index)
raw_trace['dow'] = pd.Series(index=raw_trace.index)
parsedFull = []
parsedDate = []
parsedToD = []
parsedDoW = []
for item in raw_trace['stamp'].loc[raw_trace['stamp'].notnull()]:
    item = pd.to_datetime(((item -25569)*86400).astype('int'),unit='s')
    parsedFull.append(item) #Datetime
    parsedDate.append(item.strftime('%Y-%m-%d')) #String
    parsedToD.append(item.strftime('%H:%M:%S')) #String
    parsedDoW.append(item.weekday())

raw_trace['time'].loc[raw_trace['stamp'].notnull()] = parsedFull
raw_trace['date'].loc[raw_trace['stamp'].notnull()] = parsedDate
raw_trace['tod'].loc[raw_trace['stamp'].notnull()] = parsedToD
raw_trace['dow'].loc[raw_trace['stamp'].notnull()] = parsedDoW
raw_trace['weekday'] = raw_trace['dow'] > 4

'''==========================='''
''' Combining Traces/Checkins '''
'''==========================='''

raw_callLog = pd.read_csv('01_checkin.csv',
                          usecols = ['device_id','time','date','tod','dow','weekday','stamp',
                                     'current_lat','current_lon',
                                     'stop_id','stop_lat','stop_lon',
                                     'fav','route_list','route_cnt','agency_id'],
                          parse_dates= ['time'],
                          infer_datetime_format= True,
                          index_col = None)

raw_callLog['source'] = 'checkin'

# output data (call logs and traces) from IDs with tracing records
fltr_callLog = raw_callLog[raw_callLog['device_id'].isin(raw_trace['device_id'])]
shared = pd.concat([raw_trace,fltr_callLog],
                   axis=0,
                   join='outer')
shared['time'] = pd.to_datetime(shared['time'],
                                format="%Y-%m-%d %H:%M:%S",
                                errors='coerce')
shared.sort_values(by=['device_id','time'])
shared.to_csv('shared.csv',
              date_format='%Y-%m-%d %H:%M:%S',
              index=False)


# output data (call logs and traces) from all IDs
merged = pd.concat([raw_trace,raw_callLog],
                   axis=0,
                   join='outer')

merged['time'] = pd.to_datetime(merged['time'],
                                format="%Y-%m-%d %H:%M:%S",
                                errors='coerce')

merged.sort_values(by=['device_id','time'])
merged.to_csv('merged.csv',
              date_format='%Y-%m-%d %H:%M:%S',
              index=False)
# mark fav stops in traces


# filter users with traces






