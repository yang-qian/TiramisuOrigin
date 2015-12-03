import pandas

#df = pandas.read_csv('01_trace2014.csv')
#df = df.sort(['date', 'device_id', 'origin_id', 'time'])
#df.to_csv('01_trace2014_sorted.csv', index=False)

fout = open('01_trace2014_first.csv', 'w')
with open('01_trace2014_sorted.csv') as fin:
    for line in fin:
        print >> fout, line.rstrip() # header line
        break
    pre_date, pre_device_id, pre_origin_id = None, None, None
    for line in fin:
        splited = line.rstrip().split(',')
        date, device_id, origin_id = splited[14], splited[15], splited[8]
        if (pre_date, pre_device_id, pre_origin_id) != (date, device_id, origin_id):
            print date, device_id, origin_id
            print >> fout, line.rstrip()
            pre_date, pre_device_id, pre_origin_id = date, device_id, origin_id

fout.close()
