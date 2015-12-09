import numpy
import pandas
import random
import math
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVR
from sklearn.linear_model import Perceptron


FOLDS = 5

def dist(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

#df = pandas.read_csv('01_log_no_dup.csv')
#df = df[df.apply(lambda r: r['stop_lat'] != 'NAN', axis=1)]
#df = df[df.apply(lambda r: r['weekend'] == False, axis=1)]
#df['hour'] = df.apply(lambda r: int(float(r['tod'])), axis = 1)
#df['group'] = [int(random.random() * FOLDS) for r in xrange(len(df))]
#df['dist'] = l = df.apply(lambda r:
#                           dist(float(r['current_lat']),
#                                float(r['current_lon']),
#                                float(r['stop_lat']),
#                                float(r['stop_lon'])), axis=1)
#df.to_csv('log_distance_train.csv', index=False)

df = pandas.read_csv('log_distance_train.csv')

def SVR_rbf_wrapper():
    return SVR(kernel='rbf', C=1e3, gamma=0.1)

def SVR_linear_wrapper():
    return SVR(kernel='linear', C=1e3)

def Perceptron_wrapper():
    return Perceptron(fit_intercept=False, n_iter=10, shuffle=False)

def LogiWrapper():
    return LogisticRegression()

xColumns = [
                'current_lat',
                'current_lon',
                'hour'
            ]
yColumn = 'dist'

for f in (
                #[Perceptron_wrapper]
                LogiWrapper,
                SVR_rbf_wrapper,
                SVR_linear_wrapper
            ):
    # for each classifier
    clf = f()
    print str(clf.__class__).split(' ')[1].rstrip('>').strip('\'').split('.')[-1]
    error = 0
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
            error += (yHat[j] - yTest[j]) ** 2
    print 'total: %d, avg error %f' % (len(df), math.sqrt(error) / len(df))

