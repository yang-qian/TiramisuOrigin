import math
import pandas
from sklearn.neighbors import BallTree

RADIUS = 0.01
LIST_SIZE = 5
df = pandas.read_csv('log_distance_train.csv')

points = []
id_to_stop_id = {}
with open('stops_scores.txt') as fin:
    fin.readline()
    for i, line in enumerate(fin):
        stop_id, lat, lon, route_count, popularity = line.rstrip().split(',')
        lat, lon = float(lat), float(lon)
        route_count, popularity = int(route_count), int(popularity)
        id_to_stop_id[i] = (stop_id, lat, lon, route_count, popularity)
        points.append([lat, lon])

tree = BallTree(points)

def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def get_largest_n(l, k, num):
    if not l:
        return []
    return [x[0] for x in sorted(l, key=lambda t:t[k], reverse=True)[:num]]

hit_nearest = hit_route = hit_popu = lost_dueto_radius = 0
for i, (actual_stop, lat, lon, stop_lat, stop_lon) in enumerate(zip(df['stop_id'], df['current_lat'], df['current_lon'], df['stop_lat'], df['stop_lon'])):
    stops = tree.query_radius([lat, lon], r=RADIUS)[0]
    print i, len(stops)
    l = [(id_to_stop_id[s][0], dist(lat, lon, id_to_stop_id[s][1], id_to_stop_id[s][2]), id_to_stop_id[s][3], id_to_stop_id[s][4]) for s in stops]
    if actual_stop in get_largest_n(l, 1, LIST_SIZE):
        hit_nearest += 1
    if actual_stop in get_largest_n(l, 2, LIST_SIZE):
        hit_route += 1
    if actual_stop in get_largest_n(l, 3, LIST_SIZE):
        hit_popu += 1
    if dist(lat, lon, stop_lat, stop_lon) > RADIUS:
        lost_dueto_radius += 1

print 'total', len(df)
print 'nearest', hit_nearest
print 'route count', hit_route
print 'popularity', hit_popu
print 'lost due to small radius', lost_dueto_radius
