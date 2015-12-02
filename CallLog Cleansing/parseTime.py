import pandas as pd
from pandas import MultiIndex
import numpy as np

import re as regex
import time
import datetime
import random

import math


# input a UNIX string or float or int
# output a full time stamp
def parseDate(stamp): 
    insec = float(stamp)/1000.0
    time = datetime.datetime.fromtimestamp(insec)
    return time

def parseTime(timeStr):
    timeStr = str(timeStr)
    return datetime.datetime.strptime(timeStr,'%H:%M:%S').time()



# input a full time stamp (str)
# output a date string / a time-of-day string
def fulltoDate(fullstr):
    fullStr = pd.to_datetime(fullStr, format="%Y-%m-%d %H:%M:%S")
    date = fullstr.strftime('%Y-%m-%d')
    return date

def fulltoToD(fullStr):
    fullStr = pd.to_datetime(fullStr, format="%Y-%m-%d %H:%M:%S")
    tod = fullStr.strftime('%H:%M:%S')
    return tod
