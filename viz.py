import numpy as np
import pandas as pd
from pandas import MultiIndex

import re as regex
import datetime
import random

import math
import matplotlib.pyplot as plt

import csv

raw = pd.read_csv('00_checkin_raw.csv',na_values = "NaN")

def device_id_hist(col):
    plt.figure()
    device_id_hist =col.plot(kind='hist', bins=50, alpha = 0.5)
    time_of_day_hist.set_ylabel('check-in record count')
    time_of_day_hist.set_xlabel('device_id')
    plt.show()


day_of_week_hist(raw['day_of_week'])
