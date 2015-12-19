

fout = open('03_autofav_no_dup.csv', 'w')
with open('02_autofav.csv') as fin:
    for line in fin:
        print >> fout, line.rstrip() + ',dup_cnt' # header line
        break
    pre_line, pre_date, pre_device_id, pre_stop_id = None, None, None, None
    cnt = 0
    for line in fin:
        splited = line.rstrip().split(',')
        date, device_id, stop_id = splited[1][:10], splited[0], splited[5]
        if (pre_date and pre_stop_id and pre_device_id == device_id and date == pre_date and pre_stop_id == stop_id):
            cnt += 1
        else:
            # if cnt > 1: # for debugging
            #     print pre_device_id, pre_date, pre_stop_id
            if pre_line:
                print >> fout, pre_line + ',' + str(cnt)
            pre_line = line.rstrip()
            cnt = 1
        pre_device_id, pre_date, pre_stop_id = device_id, date, stop_id
    if pre_line:
        print >> fout, pre_line + ',' + str(cnt)

fout.close()
