import math
import pandas
import collections
from sklearn.neighbors import BallTree

#df = pandas.read_csv('log_distance_train.csv')
#df = df.sort(['device_id', 'stamp'])
#df.to_csv('log_distance_train.csv', index=False)

TRAIN_PERCENTAGE = 0.6
DISTANCE_FACTOR = 0.75 # distance boundary = 3/4 pecentile of distance history
RADIUS = 0.01
LIST_SIZE = 5
df = pandas.read_csv('03_autofav_no_dup.csv') #log file, Chi:log_distance_train.csv

test_devices = {} # all the devices with more than 10 records
with open('test_devices.csv') as fin:
    line = fin.readline()
    for line in fin:
        splited = line.rstrip().split(',')
        test_devices[splited[0]] = int(splited[1])

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

def make_reverse_tuple(t, keys):
    return tuple(-t[k] for k in keys)

# sort by keys, all desc
def get_largest_n(l, keys, num):
    if not l:
        return []
    return [x[0] for x in sorted(l, key=lambda t:make_reverse_tuple(t,keys))[:num]]

fout = open('prediction_result.csv', 'w') # prediction results
print >> fout, 'device_id,total,train,test,global_nearest,global_route,global_popu,global_lost,per_radius,per_nearest,per_route,per_popu,per_lost,train_distances'
pre = None
total=train=test=cnt=global_nearest=global_route=global_popu=global_lost=per_nearest=per_route=per_popu=per_lost = 0
distances = []
for i, (device_id, actual_stop, lat, lon, stop_lat, stop_lon) in enumerate(zip(df['device_id'], df['stop_id'], df['current_lat'], df['current_lon'], df['stop_lat'], df['stop_lon'])):
    print i
    if device_id not in test_devices:
        continue
    if device_id != pre:
        if pre:
            print >> fout, '%s,%d,%d,%d,%d,%d,%d,%d,%f,%d,%d,%d,%d,"%s"' % (pre,total,train,test,global_nearest,global_route,global_popu,global_lost,per_radius,per_nearest,per_route,per_popu,per_lost,distances)
        global_nearest=global_route=global_popu=global_lost=per_nearest=per_route=per_popu=per_lost = cnt=0
        total = test_devices[device_id]
        train = int(total * TRAIN_PERCENTAGE)
        test = total - train
        distances = []
        per_stops_popu = collections.defaultdict(int)
    distance = dist(lat, lon, stop_lat, stop_lon)
    if cnt < train:
        per_stops_popu[actual_stop] += 1
        distances.append(distance)
    else:
        if cnt == train:
            idx = int(len(distances) * DISTANCE_FACTOR)
            if idx >= int(len(distances)):
                idx = -1 
            per_radius = sorted(distances)[idx]
        # global
        stops = tree.query_radius([lat, lon], r=RADIUS)[0]
        l = [(id_to_stop_id[s][0], dist(lat, lon, id_to_stop_id[s][1], id_to_stop_id[s][2]), id_to_stop_id[s][3], id_to_stop_id[s][4]) for s in stops]
        if actual_stop in get_largest_n(l, [1], LIST_SIZE):
            global_nearest += 1
        if actual_stop in get_largest_n(l, [2], LIST_SIZE):
            global_route += 1
        if actual_stop in get_largest_n(l, [3], LIST_SIZE):
            global_popu += 1
        if distance > RADIUS:
            global_lost += 1
        # personalized
        stops = tree.query_radius([lat, lon], r=per_radius)[0]
        l = [(id_to_stop_id[s][0], dist(lat, lon, id_to_stop_id[s][1], id_to_stop_id[s][2]), id_to_stop_id[s][3], id_to_stop_id[s][4], per_stops_popu[s]) for s in stops]
        if actual_stop in get_largest_n(l, [1], LIST_SIZE):
            per_nearest += 1
        if actual_stop in get_largest_n(l, [2], LIST_SIZE):
            per_route += 1
        # sort by personalized popularity desc, then global popularity desc
        if actual_stop in get_largest_n(l, [4, 3], LIST_SIZE): 
            per_popu += 1
        if distance > per_radius:
            per_lost += 1
    cnt += 1
    pre = device_id
    
if pre:
    print >> fout, '%s,%d,%d,%d,%d,%d,%d,%d,%f,%d,%d,%d,%d,"%s"' % (pre,total,train,test,global_nearest,global_route,global_popu,global_lost,per_radius,per_nearest,per_route,per_popu,per_lost,distances)
