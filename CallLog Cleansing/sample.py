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

'''========================='''
''' Func: Sample Explortary '''
'''========================='''

# Sampling code in '03_merge_n_divide.py'
sample = []

def exploreOneID(deviceID):
    sample = pd.read_csv('sample_' + str(deviceID) + '.csv',
                      dtype ={'fav': bool , 'distance': float},
                      na_values = 'FALSE',
                      index_col = None,
                      keep_date_col=True,
                      parse_dates= 'time',
                      date_parser=lambda x: pd.to_datetime(x, format="%m/%d/%Y  %H:%M:%S"), )
    # unique values
    unique_device_count = pd.Series.value_counts(sample['device_id'])
    unique_stop_count = pd.Series.value_counts(sample['stop_id'], sort = False)
    unique_date_count = pd.Series.value_counts(sample['date'], sort = False)
    # count bus stop coverage & frequency
    print ('%s checked in these stops:' %deviceID)
    print (unique_stop_count)

    # plot date & log frequency
    plt.style.use('ggplot')
    unique_date_count.plot(alpha = 0.5)
    plt.title('How many stops checked per day by %s?' %deviceID, fontsize = 12)
    plt.savefig('%s/dateNlog.png' %deviceID)
    #plt.show()
    plt.close()

    # plot date & distance
    dates = pd.Series([pd.to_datetime(date) for date in sample['date']])
    plt.plot_date(dates, sample['distance'])
    plt.title ('Date ~ Distance, Device:%s?' %deviceID, fontsize=12)
    #plt.autofmt_xdate()
    plt.savefig('%s/dateNdistance.png' %deviceID)
    plt.show()
    plt.close()

    # plot time_of_day & distance
    tods = pd.Series([pd.to_datetime(date) for date in sample['tod']])
    plt.plot_date(tods, sample['distance'])
    plt.title ('Time of Day ~ Distance, Device:%s?' %deviceID, fontsize=12)
    #plt.autofmt_xdate()
    plt.savefig('%s/todNdistance.png' %deviceID)
    plt.show()
    plt.close()

    # Distance and bus stops
    id_grouped = sample.groupby('stop_id')

    #Figure out number of rows needed for 2 column grid plot
    #Also accounts for odd number of plots
    nrows = int(math.ceil(len(id_grouped)/2.))
    fig, axs = plt.subplots(nrows,2)
    for (i,j), ax in zip(id_grouped, axs.flat):
        # i is stop_id
        j.plot(x='time',y='distance', ax=ax)
        ax.set_title('bus stop ID: %s'%i, fontsize = 10)
        ax.grid(True)
        ax.set_xticklabels([])
        ax.legend(loc=4,prop={'size':7})
    plt.tight_layout()
    plt.savefig('%s/stopNdistance.png' %deviceID)
    plt.show()
    plt.close()

'''====================='''
''' Func: Sample A Date '''
'''====================='''

def exploreOneDayOneID(deviceID,row1,row2,date):
    DataOneDay = sample[row1:row2]
    tods = pd.Series([pd.to_datetime(date) for tod in DataOneDay['tod']])

    # plot time of day and distance
    plt.plot_date(tods,
                  DataOneDay['distance'],
                  fmt = 'bo-',
                  color = 'blue',
                  alpha = 0.5)
    plt.xlabel("time at %s,2014" %date)
    plt.ylabel("distance")
    plt.show()
    plt.savefig('%s/todNdistance.png' %deviceID)
    plt.close()

    # plot distance and stop_id in map
    DataOneDay = DataOneDay.groupby('stop_id')
    for astop in DataOneDay.groups.keys():
        dfSlice = DataOneDay.get_group(astop)
        plt.scatter(dfSlice['current_lat'], dfSlice['current_lon'],
                    s = dfSlice['distance'] * 300,
                    label = astop,
                    facecolors = 'none',
                    edgecolors = np.random.rand(3,),
                    alpha = 0.1)
    plt.legend()
    plt.title('location ~ size: distance', fontsize = 10)
    plt.show()
    plt.savefig('%s/mapNdistance.png' %deviceID)
    plt.close()

