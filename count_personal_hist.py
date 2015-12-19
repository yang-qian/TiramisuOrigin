import pandas as pd

'''
cv = pd.read_csv('cv.csv')
dev = pd.read_csv('dev.csv')
test = pd.read_csv('test.csv')
'''
df = pd.read_csv('../selected/cv_weka_selected.csv')

def count(df):
    df = df.sort(['device_id','wnum','dow','tod'])
    use_cnt = []
    cnt = 0
    pre_id = None
    for index, row in df.iterrows():
        this_id = row['device_id']
        use_cnt.append(cnt)
        if pre_id and pre_id != this_id:
            cnt = 0
        else:           
            cnt += 1
        pre_id = this_id
    df['use_cnt'] = pd.Series(use_cnt, index=df.index)
    return df
            
count(df).to_csv('../selected/cv_weka_selected_plus.csv', index=False)
