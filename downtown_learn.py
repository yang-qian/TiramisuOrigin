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
