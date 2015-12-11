import pandas
import collections

#df = pandas.read_csv('log_distance_train.csv')
#df = df.sort(['device_id', 'stamp'])
#df.to_csv('log_distance_train.csv', index=False)

q = collections.deque()
pre_device_id = None

def print_q(q, device_id, header):
    return # remove this line to print splited records to files
    if not q:
        return
    with open('data_%s.csv' % device_id, 'w') as fout:
        print >> fout, header
        while q:
            print >> fout, q.popleft()

fout = open('device_record_count.csv', 'w')
print >> fout, 'device_id,count'
with open('log_distance_train.csv') as fin:
    header = fin.readline().rstrip()
    cnt = 0
    for line in fin:
        device_id = line.rstrip().split(',')[0]
        if device_id != pre_device_id and pre_device_id:
            print_q(q, pre_device_id, header)
            print >> fout, '%s,%d' % (pre_device_id, cnt)
            cnt = 0
        q.append(line.rstrip())
        cnt += 1
        pre_device_id = device_id

print_q(q, pre_device_id, header)
print >> fout, '%s,%d' % (pre_device_id, cnt)
fout.close()
