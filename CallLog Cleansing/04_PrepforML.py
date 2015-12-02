import pandas as pd
from pandas import MultiIndex
import numpy as np

import re as regex
import time
import datetime
import random

import math
import matplotlib
import matplotlib.pyplot as plt

import parseTime as pt

'''=========================='''
''' IMPORT AND PARSE TIMEDATE'''
'''=========================='''

# import the combined data
full = pd.read_csv('full.csv',
                   dtype ={'stamp': float, 'fav': bool,'stop_id': str, 'dow': float},
                   usecols=['device_id', 'stamp','date','numToD','dow', 'weekday', 'stop_id', 'fav', 'stop_lat', 'stop_lon', 'current_lat', 'current_lon', 'distance', 'timeDif','time'],
                   parse_dates= ['date','time'],
                   infer_datetime_format= True,
                   index_col = None)


# apply parseDate function to non-NA dates
full['numToD'] = pd.Series()
parsedDate = []
parsedToD = []
for item in full['stamp'].loc[full['stamp'].notnull()]:
    item = pt.parseDate(item)
    numToD = item.hour + (item.minute/60) + (item.second/60/60)
    parsedDate.append(item)
    parsedToD.append(numToD)

full.loc[full['stamp'].notnull(),'time'] = parsedDate
full.loc[full['stamp'].notnull(),'numToD'] = parsedToD


'''=================='''
''' Filter Call Logs '''
'''=================='''


# roughly filter auto call logs
autoLog = (full['fav']==True) & (full['timeDif']< 1000) & (full['device_id'] == full['device_id'].shift(-1))
coarse = full[np.invert(autoLog)]
coarse.to_csv('coarse/coarse.csv', index=False)

# divide raw merged data into three sets
rows = coarse.index
random.shuffle(list(rows))
coarse.reindex(rows)
aSlice = int(len(coarse)*0.1)
coarse_test = coarse[:aSlice]
coarse_dev = coarse[aSlice:aSlice*3]
coarse_cv = coarse[aSlice*3:]
print (len(coarse_test)+ len(coarse_dev)+ len(coarse_cv), len(coarse))

coarse_test.to_csv('coarse/coarse_test.csv', index=False)
coarse_dev.to_csv('coarse/coarse_dev.csv', index=False)
coarse_cv.to_csv('coarse/coarse_cv.csv', index=False)






