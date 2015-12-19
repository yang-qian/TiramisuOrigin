import pandas
import collections, itertools
import numpy as np

dev_ratio = 0.2
cv_ratio = 0.9
df = pandas.read_csv('03_autofav_no_dup_new.csv')
df = df.sort(['device_id','stamp'], ascending=False)
df.to_csv('03_autofav_no_dup_new.csv', index=False)

q = collections.deque()
qtrain = collections.deque()
pre_device_id = None

# output trainset per device
def print_q(qtrain, devfile_id, header, cnt):
    if not qtrain:
        return
    with open('per_device/dev/dev_%s.csv' % devfile_id, 'w') as fout:
        print >> fout, header
        while qtrain:
            print >> fout, qtrain.popleft()
    fout.close()
    dev = pandas.read_csv('per_device/dev/dev_%s.csv' % devfile_id)[:int(dev_ratio * cnt)]
    cv = pandas.read_csv('per_device/dev/dev_%s.csv' % devfile_id)[:int(cv_ratio * cnt)]
    test = pandas.read_csv('per_device/dev/dev_%s.csv' % devfile_id)[int(cv_ratio * cnt):]
    dev_cnt = len(dev)
    cv_cnt = len(cv)
    test_cnt =len(test)
    #dev.to_csv('per_device/dev/dev_%s.csv'% devfile_id, index=False)
    #dev.to_csv('per_device/cv/cv_%s.csv'% devfile_id, index=False)
    #dev.to_csv('per_device/test/test_%s.csv'% devfile_id, index=False)
    return '%s,%s,%s' %(dev_cnt,cv_cnt,test_cnt)

# output trainset per device
def print_qtrain(q, device_id, header, cnt):
    global dev_ratio
    global cv_ratio
    i = dev_cnt = cv_cnt = test_cnt = 0
    cnt = float(cnt)
    if not q:
        return
    with open('personalized/dev.csv', 'a+') as fdev, open('personalized/cv.csv', 'a+') as fcv, open('personalized/test.csv', 'a+') as ftest:
        while np.divide(i,cnt) <= dev_ratio:
            print 'hit-dev',i,np.divide(i,cnt)
            print >> fdev, q.popleft()
            i += 1
            dev_cnt += 1
        while dev_ratio < np.divide(i,cnt) <= cv_ratio and q:
            print >> fcv, q.popleft()
            print 'hit-cv',i,np.divide(i,cnt)
            i += 1
            cv_cnt += 1
        while np.divide(i,cnt) > dev_ratio and q:
            print >> ftest, q.popleft()
            print 'hit-test',i,np.divide(i,cnt)
            i +=1
            test_cnt += 1
    return '%s,%s,%s' %(dev_cnt,cv_cnt,test_cnt)

fout = open('personalized/test_device_list.csv', 'w')
print >> fout, 'device_id,all_cnt,dev_cnt,cv_cnt,test_cnt'
with open('03_autofav_no_dup_new.csv') as fin:
    header = fin.readline().rstrip()
    cnt = 0
    for line in fin:
        # device_id = 1st col of log file
        device_id = line.rstrip().split(',')[0]
        if device_id != pre_device_id and pre_device_id:
            set_cnt = print_q(q, pre_device_id, header,cnt) # print csv per device
            #set_cnt = print_qtrain(qtrain, pre_device_id, header, cnt)
            print >> fout, '%s,%d,%s' % (pre_device_id, cnt, set_cnt)
            cnt = 0
        q.append(line.rstrip())
        # Caution! Run one append a time
        #qtrain.append(line.rstrip())
        cnt += 1
        pre_device_id = device_id
set_cnt = print_q(q, pre_device_id, header, cnt)
#set_cnt = print_qtrain(qtrain, pre_device_id, header, cnt)
print >> fout, '%s,%d, %s' % (pre_device_id, cnt, set_cnt)


# write header to cv/val/test file
def add_header(setname,header):
    for aset in setname:
        with open('personalized/%s.csv'% aset, 'r+') as f:
            content = f.read()
            f.seek(0,0)
            f.write(header + '\n' + content)
#add_header(['dev','cv','test'], header)

fout.close()



# sort test_device_list.csv
df = pandas.read_csv('personalized/test_device_list.csv')
df = df.sort(['all_cnt'],ascending=False)
df.to_csv('personalized/test_device_list.csv', index=False)

