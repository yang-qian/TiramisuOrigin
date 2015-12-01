
# coding: utf-8

import pandas as pd
from pandas import MultiIndex
import numpy as np

import re as regex
import datetime
import random
import glob


import matplotlib.pyplot as plt

# read raw trace data file into pandas dataFrame
iter_log_csv = pd.read_csv('00_checkin_raw.csv', iterator=True, chunksize=1000,na_values=['NULL'], parse_dates=True)
raw_log = pd.concat(iter_log_csv)
raw_log = raw_log.reset_index(drop=True)


# parse urls and save in seperate csv

def parse_it(url):
    current_lat = ''
    # note that lat could be the last nugget
    current_lat = regex.findall("&latitude=(40\..\+?\d+)",url)
    current_lat = ''.join(current_lat)
    current_lon = ''.join(regex.findall("&longitude=(.+?)&",url))
    device_id = regex.findall("\&device_id=(.+?)&", url)
    stamp = regex.findall("&time=(.+?)&",url)
    # parse date format
    date = regex.findall("&date=(.+?)&",url)
    stop_id = regex.findall("&stop_id=(.+?)&",url)
    fav = regex.findall("&favorite=(.+?)&",url)
    return pd.Series([''.join(device_id),''.join(stamp),''.join(date),current_lat,float(current_lon),''.join(stop_id),''.join(fav)])

parsed_log = pd.DataFrame()

for i in range(100000):
    piece = parse_it(raw_log['url'][i])
    parsed_log = parsed_log.append(piece,ignore_index=True)
    # print i
    # print piece[3]
    if i%10000 == 0:
        print (i)

parsed_log.to_csv('temp1.csv', na_rep='FALSE', index=False)



