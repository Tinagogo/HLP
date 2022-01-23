import collections
import numpy as np
import pandas as pd

def get_features():
    '''
    See details in Features.ipynb
    '''
    X = pd.read_csv('summary_application.csv')
    del X['FLAG_MOBIL']
    print('data shape', X.shape)
    id_counts = X['ID'].value_counts()
    id_dups = id_counts.index[id_counts>1]
    X = X.loc[~X['ID'].isin(id_dups)]
    X.set_index('ID', inplace=True)
    print('data shape after removing duplicates and setting ID', X.shape)
    X = X.loc[X['CNT_CHILDREN'] <= 5]
    X['FLAG_EMPLOYED'] = X['DAYS_EMPLOYED']<0
    X.loc[~X['FLAG_EMPLOYED'], 'DAYS_EMPLOYED'] = X.loc[X['FLAG_EMPLOYED'], 'DAYS_EMPLOYED'].mean()
    print('data shape after removing outliers and adding indicators', X.shape)
    X['DAYS_EMPLOYED'] = X['DAYS_EMPLOYED'].map(lambda days: np.log(-days))
    X['AMT_INCOME_TOTAL'] = X['AMT_INCOME_TOTAL'].map(np.log10)
    X['OCCUPATION_TYPE'].fillna('Unknown', inplace=True)
    F = X.columns.str.startswith('FLAG_') & (X.dtypes != object)
    X.loc[:, F] = X.loc[:, F].astype(str)
    return X

def get_labels(defaults=['1','2','3','4','5']):
    '''
    See details in Labels.ipynb
    '''
    H = pd.read_csv('summary_credit_history.csv')
    C = H.groupby('ID')['STATUS'].value_counts().unstack(fill_value=0)
    C = C[ C.sum(axis=1)!=C['X'] ]
    C['label']=C[defaults].sum(axis=1)>0
    return C['label']

def get_dynamic_data(m=3, defaults=['1','2','3','4','5']):
    #predict the last m calendar months based previous records
    history = pd.read_csv('summary_credit_history.csv')
    
    train = history[history['MONTHS_BALANCE']<=-m]
    test = history[history['MONTHS_BALANCE']>-m]
    
    train = train.groupby('ID')['STATUS'].value_counts().unstack(fill_value=0)
    train = train[train.sum(axis=1)>m+1]
    
    test = test.groupby('ID')['STATUS'].value_counts().unstack(fill_value=0)
    test = test[test.sum(axis=1)==m]
    test['label']=test[defaults].sum(axis=1)>0

    return train, test['label']
    
def get_cumulative_data(m=3, defaults=['1','2','3','4','5']):
    #predict the last m client months based on previous records
    history = pd.read_csv('summary_credit_history.csv')
    group = history.groupby('ID')
    count = group.cumcount()
    
    train = history[count>=m]
    test = history[count<m]
    
    train = train.groupby('ID').agg(
        first_month=pd.NamedAgg(column='MONTHS_BALANCE', aggfunc='min'),
        last_month=pd.NamedAgg(column='MONTHS_BALANCE', aggfunc='max'),
        status_count=pd.NamedAgg(column='STATUS', aggfunc=collections.Counter),
    )
    train = train.query('last_month-first_month>@m')
    del train['last_month']
    status_count = pd.DataFrame(train['status_count'].to_list(), index=train.index).fillna(0)
    train = pd.concat([train, status_count], axis=1)
    del train['status_count']
    
    test=test.groupby('ID')['STATUS'].value_counts().unstack(fill_value=0)
    test['label']=test[defaults].sum(axis=1)>0

    return train, test['label']
