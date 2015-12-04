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

import sample
import parseTime as pt


'''==================='''
''' Combine Temp CSVs '''
'''==================='''

# aggregating seperate csvs
subset = [1,2,3,4,5,6]
templist = []
full = pd.DataFrame()
for i in subset:
    file ='temp%d_wStop.csv' % i
    df = pd.read_csv(file, index_col=None, na_values= 'FALSE')
    templist.append(df)
full = pd.concat(templist, axis=0, ignore_index=True)

# Parse UNIX to readable date

full['date'] = pd.Series(index=full.index)
full['tod'] = pd.Series(index=full.index)
full['numToD'] = pd.Series(index=full.index)
full['dow'] = pd.Series(index=full.index)
parsedFull = []
parsedDate = []
parsedToD = []
numToD = []
parsedDoW = []

for item in full['stamp'].loc[full['stamp'].notnull()]:
    item = pt.parseDate(item)
    parsedFull.append(item) #Datetime
    parsedDate.append(item.strftime('%Y-%m-%d')) #String
    parsedToD.append(item.strftime('%H:%M:%S')) #String
    parsedDoW.append(item.weekday())
    numToD.append(item.hour + (item.minute/60) + (item.second/60/60))
# Replace old problematic 'time' with full representation of time,
# which is parsed from UNIX stamps.
full['time'].loc[full['stamp'].notnull()] = parsedFull
full['date'].loc[full['stamp'].notnull()] = parsedDate
full['tod'].loc[full['stamp'].notnull()] = parsedToD
full['numToD'].loc[full['stamp'].notnull()] = numToD
full['dow'].loc[full['stamp'].notnull()] = parsedDoW
full['weekend'] = full['dow'] > 4

# organize data type and order
full = full.sort_values(['device_id', 'stamp'])
#full = full.groupby('device_id')

# calculate check-in gap
full['timeDif'] = full['stamp'].diff()

# differcient true and false fav column NaNs
full.loc[full['stamp'].notnull() & full['fav'].isnull(),'fav'] = False


# output csv
full.to_csv('full.csv', index=False)

# output notfull.csv: weekday data, drop problematic(csv-->arff) cols
full[full['weekend']==False].drop(['route_list','stop_location','weekend'],1).to_csv('notfull.csv', index=False)


'''==================='''
''' Sample Device IDs '''
'''==================='''

'''
# sample a device_id
sample_id = str('7fb7a0a5-b770-4149-aebb-1159b4bdb166')
sampleSet = full[full['device_id']== sample_id]
sampleSet.to_csv('sample_%s.csv'%sample_id, na_rep='FALSE', index=False)
sample.exploreOneID(sample_id)


# sample a day
sampleDate = input("Sample a date:")
row1 = input("End row")
row2 = input("Start row")
sample.exploreOneDayOneID(sample_id,row1,row2,sampleDate)
'''


