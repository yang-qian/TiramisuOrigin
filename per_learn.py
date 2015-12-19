import pandas as pd
import numpy as np
import re
from collections import Counter
from sklearn.preprocessing import normalize
import itertools as rpt

import distance as dis

stops = pd.read_csv('../stop_dict.csv',usecols=['agency_id','stop_id','stop_lat','stop_lon','route_cnt'])
stops = stops.loc[stops['agency_id']==38]

def route_freq(device_id, cv):
    # return a dict of stop-score pairs
    df = cv[['stop_id','route_list']].drop_duplicates()
    route_all = []
    score = []
    if len(df) != 0:
        for route in df['route_list']:
            route = re.findall("'(.{2,4})'",route)
            route_all.extend(route)
            route_score = Counter(route_all)
            stop_score = pd.Series.replace(pd.Series(route),route_score)
            score.append(stop_score.max())
    return dict(zip(df['stop_id'], score))

def prep(device_id):
    global stops
    stop_dict = stops
    df = pd.DataFrame()
    cv = pd.read_csv('cv/cv_%s.csv' % device_id)
    cv_cnt = len(cv)
    test = pd.read_csv('test/test_%s.csv' % device_id)
    d = route_freq(device_id,cv)
    
    for set_name in ['cv','test']:
        if set_name == 'cv':
            df = cv
        else:
            df = test
        df['route_dup_cnt'] = df['stop_id'].map(d)
        df.drop(['route_list','date','time','stamp','device_id'], axis=1, inplace=True)
        df['prob'] = True
        # repeat rows
        df = cv.reindex(np.repeat(cv.index.values,len(d)))
        df['stop_id_f'] = list(d.keys()) * cv_cnt
        df['prob'] = df['stop_id_f'] == df['stop_id']
        stop_dict = stop_dict[stop_dict['stop_id'].isin(list(d.keys()))]
        stop_dict['route_dup_cnt'] = stop_dict['stop_id'].map(d)
        #print stop_dict
        df = df.merge(stop_dict,left_on=['stop_id_f'],right_on = ['stop_id'], how='outer',sort=False,suffixes=('', 'f')).sort(['wnum','dow','tod','stop_id'])
        f = df['prob'] == False
        df.loc[f,'dup_cnt'] = 0
        df.loc[f,'fav'] = False
        df.loc[f,'stop_lat'] = df['stop_latf']
        df.loc[f,'stop_lon'] = df['stop_lonf']
        df.loc[f,'route_cnt'] = df['route_cntf']
        df.loc[f,'route_dup_cnt'] = df['route_dup_cntf']
        distance = []
        for i in range(len(df.loc[f])):
            lat1 = df.loc[i,'current_lat']
            lon1 = df.loc[i,'current_lon']
            lat2 = df.loc[i,'stop_lat']
            lon2 = df.loc[i,'stop_lon']
            distance.append(dis.dis(lat1,lon1,lat2,lon2))
        df.loc[f,'distance'] = distance
        df['stop_id'] = df['stop_idf']
        df.drop(['stop_id_f','stop_idf','stop_latf','stop_lonf','route_cntf','route_dup_cntf','agency_id'], axis=1, inplace=True)

        # save
        df['prob'] = df['prob'].map({True: 1, False : 0})
        #print df['prob'].head()
        df.to_csv('%s_weka/%s_%s.csv'%(set_name,set_name,device_id), index = False)


device = pd.read_csv('test_device_list.csv')
for did in device['device_id']:
    prep(did)
    print did

#prep('0A8F4197-B7B0-4541-8784-721753FF3183') 
