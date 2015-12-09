import math
import pandas
from rtree import index

RANGE = 0.01
LIST_SIZE = 5
p = index.Property()
p.dimension = 2
idx = index.Index(properties=p)
id_to_stop_id = {}
df = pandas.read_csv('log_distance_train.csv')

with open('stops_scores.txt') as fin:
    fin.readline()
    for i, line in enumerate(fin):
        stop_id, lat, lon, route_count, popularity = line.rstrip().split(',')
        lat, lon = float(lat), float(lon)
        route_count, popularity = int(route_count), int(popularity)
        id_to_stop_id[i] = (stop_id, lat, lon, route_count, popularity)
        idx.add(i, (lat, lon, lat, lon))

'''
for RANGE in (0.05, 0.03, 0.02, 0.015, 0.01):
    with open('count_stops_%f.csv' % RANGE, 'w') as fout:
        print >> fout, 'id,count_stops'
        for i, (lat, lon) in enumerate(zip(df['current_lat'], df['current_lon'])):
            print >> fout, '%d,%d' % (i, len(list(idx.intersection((lat - RANGE, lon - RANGE, lat + RANGE, lon + RANGE)))))
'''

def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def get_largest_n(l, k, num):
    if not l:
        return []
    return [x[0] for x in sorted(l, key=lambda t:t[k], reverse=True)[:num]]

hit_nearest = hit_route = hit_popu = 0
for i, (actual_stop, lat, lon) in enumerate(zip(df['stop_id'], df['current_lat'], df['current_lon'])):
    print i
    stops = list(idx.intersection((lat - RANGE, lon - RANGE,
                                   lat + RANGE, lon + RANGE)))
    #(stop_id, lat, lon, route_count, popularity) = id_to_stop_id[i]
    l = [(id_to_stop_id[s][0], dist(lat, lon, id_to_stop_id[s][1], id_to_stop_id[s][2]), id_to_stop_id[s][3], id_to_stop_id[s][4]) for s in stops]
    if actual_stop in get_largest_n(l, 1, LIST_SIZE):
        hit_nearest += 1
    if actual_stop in get_largest_n(l, 2, LIST_SIZE):
        hit_route += 1
    if actual_stop in get_largest_n(l, 3, LIST_SIZE):
        hit_popu += 1

print 'total', len(df)
print 'nearest', hit_nearest
print 'route count', hit_route
print 'popularity', hit_popu
