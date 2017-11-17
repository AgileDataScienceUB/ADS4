import operator

import pandas as pd
import numpy as np
import datetime as dt

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

import ML_utils as mlu

def split_dataset(df, random=True, test_size=None, sorting_field=None, value=None):
    
    if sorting_field:
        random = False
    
    assert test_size or (sorting_field and value), 'You must specify test_size or sorting_field and value.'
    assert random or sorting_field, 'You must choose between random and sorting_field.'
    assert not (test_size and value), 'You must specify test_size or value, not both.'
    
    if random:
        df2 = df.reindex(np.random.permutation(df.index))
    
    if sorting_field:
        df2 = df.sort_values(sorting_field).reset_index(drop=True).copy()
    
    if test_size:
        i = int(len(df2)*(1 - test_size))
        train = df2.iloc[:i].copy()
        test = df2.iloc[i:].copy()
    
    if value:
        train = df2.loc[df2[sorting_field] < value].copy()
        test = df2.loc[df2[sorting_field] >= value].copy()
    
    return train, test

# Weight of evidence (WOE)

def get_woe_dict(df, result, c, threshold=1e-03, n_min=100):

    mean_rate = df[result].mean()
    groups = df.groupby(by=c)
    dfx = pd.DataFrame()
    dfx['employees'] = groups.size()
    dfx['terminations'] = groups[result].sum()
    dfx['rate'] = dfx['terminations']/dfx['employees']
    dfx.loc[dfx['rate'] == 0, 'rate'] = threshold
    dfx['r'] = np.log(dfx['rate']/mean_rate)
    dfx['r_hat'] = dfx['r']*(dfx['employees']/n_min).clip_upper(1)
    d = dfx['r_hat'].to_dict()
    return d

def get_woe_series(df, c, d):
    return df[c].apply(lambda x: d.get(x, 0))

def get_X_and_y(df, indep_variables, result):
    X = df[indep_variables].as_matrix().astype(float)
    y = np.array(df[result])
    return X, y

def feature_selector(train, indep_variables, result, clf, min_gain=1e-03):
    features_to_test = indep_variables[:]
    selected_feats = []
    best_metric = 0.5
    yt = np.array(train[result])
    print 'Feature selection algorithm\n{}'.format('-'*80)
    
    while len(features_to_test) > 0:
        d = {}

        for f in features_to_test:
            X = train[[f] + selected_feats].as_matrix().astype(float)
            score, _ = mlu.k_fold_cross_validation(X, yt, 5, clf)
            d[f] = roc_auc_score(yt, score)
            best_feat = max(d.iteritems(), key=operator.itemgetter(1))[0]

        current_metric = d[best_feat]
        gain = (current_metric - best_metric)/best_metric
        
        if gain > min_gain:
            best_metric = current_metric
            selected_feats.append(best_feat)
            features_to_test.remove(best_feat)
            print '+ {} (ROC AUC score inc = {:.2%})'.format(best_feat, gain)

        else:
            print '{} has been excluded (ROC AUC score inc = {:.2%})'.format(best_feat, gain)
            break
    print 'Feature selection is over.'
            
    return selected_feats

def pandoras_box(file_name, target, employee_id=None, record_id=None, hire_date=None,
                 record_date=None, termination_date=None, length_of_service=None, 
                 age=None, birth_date=None, birth_year=None, other_target_fields=[],
                 job_title=None, special_field_types={}):
    
    # Define date fields
    all_date_fields = [record_date, hire_date, termination_date, birth_date]
    date_fields = []
    for f in all_date_fields:
        if f:
            date_fields.append(f)

    # Define field types:
    field_types = {
        employee_id: str,
        record_id: str,
        length_of_service: float,
        age: float,
        birth_year: int
    }
    field_types.update(special_field_types)

    # Load dataset
    df = pd.read_csv(file_name, dtype=field_types, parse_dates=date_fields)

    # Sort by record_date
    if record_date:
        df = df.sort_values(record_date).reset_index(drop=True)
    elif hire_date:
        df.sort_values(hire_date).reset_index(drop=True)
    elif termination_date:
        df.sort_values(termination_date).reset_index(drop=True)
    elif birth_date:
        df.sort_values(birth_date).reset_index(drop=True)

    # Create record_id if necessary
    if not record_id:
        record_id = 'record_id'
        df[record_id] = df.index

    # Create result
    assert target, 'You must specify a target field.'
    result = 'result'
    target_values = np.sort(df[target].unique())
    assert len(target_values) == 2, 'There must be 2 unique values in the target field.'
    if all(target_values == np.array([0, 1])):
        df[result] = df[target]
    else:
        v = df[target].value_counts().index[1]
        df[result] = (df[target] == v).astype(int)

    if termination_date:
        df.loc[df[result] == 0, termination_date] = np.datetime64('NaT')

    # Drop target fields
    target_fields = [target] + other_target_fields
    df.drop(target_fields, axis=1, inplace=True)

    # Job title enrichment
    job_title2 = 'job_title2'
    job_title3 = 'job_title3'
    titles2 = ['analyst', 'clerk', 'director', 'exec assistant', 'manager']
    titles3 = ['accounting', 'accounts', 'audit', 'baker', 'compensation', 'dairy',
               'finance','human resources', 'investment', 'labor relations',
               'legal counsel', 'meat', 'produce', 'recruit', 'store', 'train']

    if job_title:

        df[job_title2] = df[job_title].str.lower()
        df[job_title3] = df[job_title].str.lower()

        for t in titles2:
            df.loc[df[job_title2].str.contains(t), job_title2] = t
        for t in titles3:
            df.loc[df[job_title3].str.contains(t), job_title3] = t
        print '(!) Job title enrichment has been performed.\n'

    # Length of service enrichment
    if hire_date and record_date:
        length_of_service = 'length_of_service'
        df[length_of_service] = df[record_date].subtract(df[hire_date]).dt.days
        print '(!) Length of service enrichment has been performed.\n'

    else:
        if length_of_service:
            if df[length_of_service].dtype == '<m8[ns]':
                df[length_of_service] = df[length_of_service].dt.days

    # Birth date / Age enrichment

    if age and record_date and not birth_date:
        birth_date = 'birth_date'
        df[birth_date] = df[record_date].subtract(pd.to_timedelta(df[age], unit='y'))

    if birth_date and not birth_year:
        birth_year = 'birth_year'
        df[birth_year] = df[birth_date].dt.year
        print '(!) Birth year enrichment has been performed.\n'

    g_dict = {
        'the_greatest_generation': {birth_year:(1901, 1926), age:(91, np.inf)},
        'the_silent_generation': {birth_year:(1927, 1945), age:(72, 90)},
        'the_baby_boomers': {birth_year:(1946, 1964), age:(53, 71)},
        'gen x': {birth_year:(1965, 1980), age:(37, 52)},
        'gen_y': {birth_year:(1981, 2000), age:(17, 36)},
        'gen_z': {birth_year:(2001, 2017), age:(1, 16)},
    }

    key = birth_year or age
    if key:
        generation = 'generation'
        df[generation] = ''
        for k, v in g_dict.items():
            df.loc[(df[key] >= v[key][0]) & (df[key] <= v[key][1]), generation] = k
        print '(!) Generation enrichment has been performed.\n'

    # Feature engineering
    id_fields = [employee_id, record_id]
    excluded_features = target_fields + date_fields + id_fields + [result]

    for c in [c for c in df.columns if c not in excluded_features]:

        column_values = np.sort(df[c].unique())

        # Drop columns with < 2 unique values
        if len(column_values) < 2:
            df.drop(c, axis=1, inplace=True)
        continue

        # Categorical features
        if mlu.is_categorical(df, c):
            # Fill na with blanks
            df[c].fillna('', inplace=True)

            # Value counts
            vc = df[c].value_counts(normalize=True)

            # 2-value features
            if len(vc) == 2:
                v = vc.index[-1]
                df[c] = (df[c] == v).astype(int)

            # >2-value features
            else:
                pass          
                # One hot encoder (TO DO)

        # Continuous features
        elif mlu.is_continuous(df, c):
            # Outliers detection (TO DO)
            # Missing values imputation (TO DO)
            pass

    indep_variables = [c for c in df.columns if c not in excluded_features]        

    # Split train and validation set
    train, valid = split_dataset(df, sorting_field=record_date, test_size=0.2)

    # Weight of evidence
    for c in [v for v in indep_variables if mlu.is_categorical(train, v)]:
        d = get_woe_dict(train, result, c)
        train[c] = get_woe_series(train, c, d)
        valid[c] = get_woe_series(valid, c, d)

    # Define the classifier
    clf = LogisticRegression()

    # Feature selection
    selected_feats = feature_selector(train, indep_variables, result, clf)
    assert selected_feats, 'The feature selector has excluded all independent variables. Your data is bull****.'
    
    # Predict validation set

    Xt, yt = get_X_and_y(train, selected_feats, result)
    Xv, yv = get_X_and_y(valid, selected_feats, result)

    clf.fit(Xt, yt)
    score = clf.predict_proba(Xv)[:,1]
    yhat = clf.predict(Xv)
    valid_metrics = mlu.get_metrics(yv, score, yhat)
    
    return clf, valid_metrics