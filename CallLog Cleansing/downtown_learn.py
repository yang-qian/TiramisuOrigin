import numpy
import pandas
import random
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn import svm
from sklearn import tree

def SVCWrapper():
    return svm.SVC(kernel='rbf', gamma=0.1, C=1.0, class_weight='auto')

def LinearSVCWrapper():
    return svm.LinearSVC(C=1.0, class_weight='auto')
    
def TreeWrapper():
    return tree.DecisionTreeClassifier(class_weight='auto')
    
def LogiWrapper():
    return LogisticRegression(class_weight='auto')

FOLDS = 5
with open('downtown_stops.txt') as fin:
    stops = {line.split(',')[0] for line in fin}

print 'loading dataset'
df = pandas.read_csv('01_checkin_fav.csv') # 649460 records
df = df.fillna(0)
df = df[df.apply(lambda r: r['stop_id'] in stops, axis=1)] #82835
df = df[df.apply(lambda r: r['is_fav'] == 0, axis=1)] # 33042
df = df[df.apply(lambda r: r['current_lon'] != 0, axis=1)] 
df = df[df.apply(lambda r: r['current_lat'] != 0, axis=1)] # 32438

df['hour'] = df.apply(lambda r: int(r['tod'].split(':')[0]), axis = 1)     
group = [int(random.random() * FOLDS) for r in xrange(len(df))]
df['group'] = group
stops = list(stops)
df['stop_index'] = df.apply(lambda r: stops.index(r['stop_id']), axis = 1)     

xColumns = [
                'current_lat',
                'current_lon',
                'weekday',
                'hour'
            ]
yColumn = 'stop_index'

stops = []
with open('stops.txt') as fin:
    for line in fin:
        name, lat, lont = line.rstrip().split(',')
        lat, lont = float(lat), float(lont)
        if 40.43688 <= lat <= 40.443609 and -80.00585 <= lont <= -79.995292:
            stops.append((name, lat, lont))
print '%d stops in downtown' % len(stops)

def nearest(lat, lont):
    global stops
    lat, lont = float(lat), float(lont)
    return min(((latt - lat) ** 2 + (lontt - lont) ** 2, name) for name, latt, lontt in stops)[1]

print 'calculating baseline'
baseline_actual = df['stop_id']
baseline_predict = df.apply(lambda r: nearest(r['current_lat'], r['current_lon']), axis = 1)
baseline_correct = sum(1 if a == b else 0 for a, b in zip(baseline_actual, baseline_predict))
print 'total %d, correct %d, incorrect %d, pencentage %f' % (len(baseline_actual), baseline_correct, len(baseline_actual) - baseline_correct, float(baseline_correct) / len(baseline_actual))

for f in (
                TreeWrapper,
                LogiWrapper
                #SVCWrapper, 
                #LinearSVCWrapper
            ):
    # for each classifier
    clf = f()
    print str(clf.__class__).split(' ')[1].rstrip('>').strip('\'').split('.')[-1] 
    correct = 0
    incorrect = 0
    for i in xrange(FOLDS):
        train = df[df['group'] != i]
        test = df[df['group'] == i]
        xTrain = train[xColumns]
        yTrain = numpy.array(train[yColumn])
        xTest = test[xColumns]
        yTest = numpy.array(test[yColumn])
        yHat = clf.fit(xTrain, yTrain).predict(xTest)
        # collect results
        for j in xrange(len(yHat)):
            if int(yHat[j]) == int(yTest[j]):
                correct += 1
            else:
                incorrect += 1
    print 'total: %d, correct %d, incorrect %d, pencentage %f' % (correct + incorrect, correct, incorrect, float(correct) / (correct + incorrect))
