import collections

FAV_THRESHOLD = 500 # in milliseconds

q = collections.deque()
fout = open('01_checkin_no_dup_fav.csv', 'w')
with open('01_checkin_no_dup.csv') as fin:
    for line in fin:
        print >> fout, line.rstrip() + ',is_fav' # header line
        break
    pre_date, pre_device_id, time_start = None, None, 0
    for line in fin:
        splited = line.rstrip().split(',')
        date, device_id, time = splited[1][:10], splited[0], splited[2]
        time = int(time) if time else time_start
        if pre_date == date and pre_device_id == device_id and abs(time_start - time) <= FAV_THRESHOLD:
            pass
        else:
            if len(q) > 1:
                while q:
                    print >> fout, q.popleft() + ',1'
            else:
                if len(q) == 1:
                    print >> fout, q.popleft() + ',0'
            time_start = time
        pre_date, pre_device_id= date, device_id
        q.append(line.rstrip())
    if len(q) > 1:
        while q:
            print >> fout, q.popleft() + ',1'
    else:
        if len(q) == 1:
            print >> fout, q.popleft() + ',0'

fout.close()
