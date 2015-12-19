import pandas
import collections

stop_popularity = collections.defaultdict(int)
stops = {}
df = pandas.read_csv('01_weekdaylog.csv')
df = df[df.apply(lambda r: r['time'] != 'NAN', axis=1)] 
df = df[df.apply(lambda r: r['agency_id'] != 'NAN', axis=1)] 

for stop_id, route_list, stop_lat, stop_lon in zip(df['stop_id'], df['route_list'], df['stop_lat'], df['stop_lon']):
    stop_popularity[stop_id] += 1
    stops[stop_id] = (stop_lat, stop_lon, len(route_list.split(',')))
        
with open('stops_scores.txt', 'w') as fout:
    print >> fout, 'stop_id,stop_lat,stop_lon,route_count,popularity'
    for stop_id, (lat, lont, count) in sorted(stops.items()):
        print >> fout, '%s,%s,%s,%d,%d' % (stop_id, lat, lont, count, stop_popularity[stop_id])
