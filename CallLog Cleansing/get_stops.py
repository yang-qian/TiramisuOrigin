stops = set()
with open('01_checkin.csv') as fin:
    line = fin.readline()
    for line in fin:
        splited = line.split(',')
        stop = splited[5]
        lat = splited[7]
        lont = splited[8]
        if not stop or not lat or not lont:
            continue
        assert '(' in lat
        assert ')' in lont
        lat = lat.lstrip('"(')
        lont = lont.rstrip('")')
        stops.add((stop, lat, lont))
        
with open('stops.txt', 'w') as fout:
    for stop, lat, lont in stops:
        print >> fout, '%s,%s,%s' % (stop, lat, lont)
