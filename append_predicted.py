import pandas as pd

# folder:selected
dev = pd.read_csv('dev_random.csv')

# substitute direction col with predicted values
dirc = pd.read_csv('train_direction/direction_predicted_dev_tuned.csv', usecols=['predicted'])
dev['direction'] = dirc
dev.to_csv('train_distance/dev_random_preDirc.csv', index=False)

#dist = pd.read_csv('train_distance/distance_predicted_dev.csv', usecols=['predicted'])
#dev['distance'] = dist


