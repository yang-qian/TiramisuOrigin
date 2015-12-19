import pandas as pd
from pandas import MultiIndex
import numpy as np

import re as regex
import time
import datetime
import random

import math
import parseTime as pt
import distance as dis

stops = pd.read_csv('stop_dict.csv')

'''=================='''
''' Cleansing Traces '''
'''=================='''
'''
raw_trace = pd.read_csv('full_trace.csv',
                        usecols = ['device_id','hour','minute','second','date',
                                   'current_lat','current_lon',
                                   'trip_id','origin_id','origin_lat','origin_lon',
                                   'route_short_name','source','agency_id'],
                        parse_dates=True)

raw_trace = raw_trace[raw_trace['source'] == 'recording']
raw_trace = raw_trace[raw_trace['agency_id'] == (38 or 46)]

raw_trace = raw_trace.rename(columns = {'route_short_name':'route_id'})

raw_trace = raw_trace.rename(columns = {'origin_id':'stop_id'})
raw_trace = pd.merge(raw_trace, stops, on=['stop_id','agency_id'], how='left')


raw_trace['time'] = pd.to_datetime(raw_trace['date']
                                   + raw_trace['hour'].astype(str)
                                   + raw_trace['minute'].astype(str)
                                   + raw_trace['second'].astype(str),
                                   format="%m/%d/%y%H%M%S",
                                   errors='coerce'
                                   )
raw_trace['date'] = pd.to_datetime(raw_trace['date'],format='%m/%d/%y')

raw_trace['dow'] = raw_trace['time'].apply(lambda x: x.weekday())
raw_trace['tod'] = raw_trace['hour'] + (raw_trace['minute']/60) + (raw_trace['second']/60/60)
raw_trace['weekend'] = raw_trace['dow'] > 4

raw_trace = raw_trace[(raw_trace['current_lat'] > 40.286527) & (raw_trace['current_lat'] < 40.624502)]
raw_trace = raw_trace[(raw_trace['current_lon'] > -80.05378) & (raw_trace['current_lon'] < -79.896084)]
print (len(raw_trace))

raw_trace = raw_trace.sort_values(by=['date', 'device_id', 'stop_id', 'time'])
raw_trace.to_csv('01_trace.csv',
                 date_format='%Y-%m-%d %H:%M:%S',
                 columns = ['device_id','time','date','tod','dow','weekend','stamp',
                              'current_lat','current_lon','distance',
                              'stop_id','direction','stop_lat','stop_lon',
                              'fav','route_cnt','route_list'],
                 index=False,
                 na_rep = 'NAN')
'''                
'''====================='''
''' Cleansing Call logs '''
'''====================='''

raw_callLog = pd.read_csv('full_log.csv',
                          usecols = ['device_id','stamp','time','date','tod','dow','weekend','stamp',
                                     'current_lat','current_lon',
                                     'stop_id','stop_lat','stop_lon',
                                     'fav','agency_id','route_cnt','route_list'],
                          parse_dates= ['time'],
                          infer_datetime_format= True,
                          index_col = None)

# raw_callLog['source'] = 'checkin'
direction = pd.read_csv('stop_direction.csv',
                        index_col = False,
                        dtype = {'stop_id':str, 'direction':float})
raw_callLog = pd.merge(raw_callLog, direction, on='stop_id', how='outer')

raw_callLog['time'] = pd.to_datetime(raw_callLog['time'],
                                     format="%Y-%m-%d %H:%M:%S",
                                     errors='coerce')

raw_callLog['tod'] = raw_callLog['time'].map(lambda x: x.hour + (x.minute/60) + (x.second/60/60))
raw_callLog['wnum'] = raw_callLog['time'].dt.week

distance = []
for i in range(len(raw_callLog)):
    lat1 = raw_callLog.loc[i,'current_lat']
    lon1 = raw_callLog.loc[i,'current_lon']
    lat2 = raw_callLog.loc[i,'stop_lat']
    lon2 = raw_callLog.loc[i,'stop_lon']
    distance.append(dis.dis(lat1,lon1,lat2,lon2))
raw_callLog['distance'] = distance

# cleansing current location geo-range
raw_callLog = raw_callLog[(raw_callLog['current_lat'] > 40.286527) & (raw_callLog['current_lat'] < 40.624502)]
raw_callLog = raw_callLog[(raw_callLog['current_lon'] > -80.05378) & (raw_callLog['current_lon'] < -79.896084)]

print (len(raw_callLog))

raw_callLog = raw_callLog[raw_callLog['stop_id'].notnull() & raw_callLog['time'].notnull()]
raw_callLog = raw_callLog[raw_callLog['distance'].notnull()]
raw_callLog = raw_callLog[raw_callLog['weekend'] == False]
print (len(raw_callLog))

raw_callLog = raw_callLog.sort_values(by=['device_id','date','time','stop_id'])
raw_callLog.to_csv('01_weekdaylog.csv',
                   date_format='%Y-%m-%d %H:%M:%S',
                   columns = ['device_id','time','stamp','date','tod','dow',
                              'current_lat','current_lon','distance',
                              'stop_id','direction','stop_lat','stop_lon',
                              'fav','route_cnt','route_list','wnum'],
                   index=False,
                   na_rep = 'NAN')


'''==========================='''
''' Combining Traces/Checkins '''
'''==========================='''
'''
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
              index=False,
              na_rep = 'NAN')

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
              na_rep = 'NAN',
              index=False,)
'''


