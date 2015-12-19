import pandas as pd
import numpy.random as random

df = pd.read_csv('personalized/test_device_list.csv', usecols =['device_id']) # already sorted by descending all_cnt
cv = pd.read_csv('personalized/cv.csv')
dev = pd.read_csv('personalized/dev.csv')
test = pd.read_csv('personalized/test.csv')

# Randomly select 200 users
'''
selected = df.ix[random.random_integers(0,len(df),200)]
selected = selected['device_id'].values.tolist()

cv[cv['device_id'].isin(selected)].sort(['wnum','dow','tod']).to_csv('random200/cv_random_4.csv', index = False)
dev[dev['device_id'].isin(selected)].sort(['wnum','dow','tod']).to_csv('random200/dev_random_4.csv', index = False)
test[test['device_id'].isin(selected)].sort(['wnum','dow','tod']).to_csv('random200/test_random_4.csv', index = False)

# Select 200 users with no data in cv&dev set
new = df.ix[random.random_integers(3985,len(df),200)]
new = new['device_id'].values.tolist()
cv[cv['device_id'].isin(new)].sort(['wnum','dow','tod']).to_csv('new_users/cv_new.csv', index = False)
dev[dev['device_id'].isin(new)].sort(['wnum','dow','tod']).to_csv('new_users/dev_new.csv', index = False)
test[test['device_id'].isin(new)].sort(['wnum','dow','tod']).to_csv('new_users/test_new.csv', index = False)
'''
'''
# Select 50 users with 1 row in cv set
onehist = df.ix[random.random_integers(3397,len(df),50)]
onehist = onehist['device_id'].values.tolist()
df_cv[df_cv['device_id'].isin(onehist)].sort(['wnum','dow','tod']).to_csv('selected/cv_weka_50newuser.csv', index = False)
df_dev[df_dev['device_id'].isin(onehist)].sort(['wnum','dow','tod']).to_csv('selected/dev_weka_50newuser.csv', index = False)
'''

# Select 50 users with more than 10 records, 7 of which in cv
tenhist = df.ix[random.random_integers(0,2062,50)]
tenhist = tenhist['device_id'].values.tolist()
cv[cv['device_id'].isin(tenhist)].sort(['wnum','dow','tod']).to_csv('selected/cv_weka_50olduser.csv', index = False)
dev[dev['device_id'].isin(tenhist)].sort(['wnum','dow','tod']).to_csv('selected/dev_weka_50olduser.csv', index = False)
test[test['device_id'].isin(tenhist)].sort(['wnum','dow','tod']).to_csv('selected/test_weka_50olduser.csv', index = False)
