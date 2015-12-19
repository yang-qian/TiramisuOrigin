import collections
import pandas


# sort by time and device
df = pandas.read_csv('01_weekdaylog.csv')
df = df.sort(['device_id', 'stamp'])
df.to_csv('01_weekdaylog.csv', index=False)


# tag fav autolog
FAV_THRESHOLD = 500 # in milliseconds

def print_q(q, fout):
    if len(q) == 1:
        print >> fout, q.popleft()[0] + ',0'
        return
    line = None
    dist = float('inf')
    while q:
        tmp_line, tmp_dist = q.popleft()
        if tmp_dist < dist:
            dist = tmp_dist
            line = tmp_line
    if line:
        print >> fout, line + ',1'

q = collections.deque()
fout = open('02_autofav.csv', 'w')
with open('01_weekdaylog.csv') as fin:
    for line in fin:
        print >> fout, line.rstrip() + ',auto_fav' # header line
        splited = line.rstrip().split(',')
        assert splited[8] == 'distance'
        break
    pre_date, pre_device_id, time_start = None, None, 0
    for line in fin:
        splited = line.rstrip().split(',')
        date, device_id, time, dist = splited[3], splited[0], splited[2], splited[8]
        time = float(time) if time else time_start
        dist = float(dist) if dist else float('inf')
        if pre_date == date and pre_device_id == device_id and abs(time_start - time) <= FAV_THRESHOLD:
            pass
        else:
            print_q(q, fout)
            time_start = time
        pre_date, pre_device_id= date, device_id
        q.append((line.rstrip(), dist))
    print_q(q, fout)

fout.close()
