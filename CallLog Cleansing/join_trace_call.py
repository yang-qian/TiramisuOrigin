import pandas
from datetime import datetime

d = {}
with open('01_trace2014_first.csv') as fin:
    for line in fin:
        columns = [(i, x) for i, x in enumerate(line.rstrip().split(','))]
        break
    for line in fin:
        splited = line.rstrip().split(',')
        date, device_id, origin_id = splited[14], splited[15].lower(), splited[8]
        date = datetime.strptime(date, "%m/%d/%y").strftime('%Y-%m-%d')
        d[(date, device_id, origin_id)] = tuple(line.rstrip().split(','))

new_columns = [[] for i, x in columns]
df = pandas.read_csv('01_checkin.csv')
for date, device_id, stop_id in zip(df['date'], df['device_id'], df['stop_id']):
    if (date, device_id, stop_id) in d:
        for i, x in enumerate(d[(date, device_id, stop_id)]):
            new_columns[i].append(x)
    else:
        for c in new_columns:
            c.append(None)

for i, x in columns:
    df['trace_' + x] = new_columns[i]

df.to_csv('call_trace_joined.csv', index=False)
