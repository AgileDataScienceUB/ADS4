# Imports

import operator

import numpy as np

from sklearn import cross_validation
from sklearn import metrics
from sklearn.preprocessing import StandardScaler


def get_X_and_y(df, indep_variables, result):
    X = df[indep_variables].as_matrix().astype(float)
    y = np.array(df[result])
    return X, y


def split_dataset(df, random=True, test_size=None, sorting_field=None, value=None):
    '''
    Split dataset in two subsets: train and validation. Before the split, the dataset is sorted:
        - randomly
        - by sorting_field
    The split is determined by:
        - test_size
        - value (if sorting_field)
    '''
    
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


def k_fold_cross_validation(X, y, k, clf, shuffle=True, random_state=None):
    '''
    Perform a k-fold cross validation for a classifier. 
    For the whole dataset, return:
        - Score (predict_proba)
        - Prediction (predict)
    '''
    
    # GroupKFold by employee_id if employee_id (TO DO)
    cv = cross_validation.KFold(X.shape[0], n_folds=k, shuffle=shuffle, random_state=random_state)
    score = np.zeros((X.shape[0], 1))
    yhat = np.zeros((X.shape[0], 1))
    
    for train_idx, test_idx in cv:
        X_train,y_train = X[train_idx,:], y[train_idx]
        X_test,y_test = X[test_idx,:], y[test_idx]
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        clf.fit(X_train_scaled, y_train)
        X_test_scaled = scaler.transform(X_test)
        score[test_idx] = clf.predict_proba(X_test_scaled)[:, 1].reshape(-1, 1)
        yhat[test_idx] = clf.predict(X_test_scaled).reshape(-1, 1)

    return score, yhat


def get_metrics(y, score, yhat):
    '''
    Return the resulting metrics of the validation of a classifier.
        - Log loss
        - Accuracy score
        - ROC AUC score
    '''
    
    metrics_dict = {}
    metrics_dict['log_loss'] = metrics.log_loss(y, score)
    metrics_dict['accuracy'] = metrics.accuracy_score(y, yhat)
    metrics_dict['roc_auc'] = metrics.roc_auc_score(y, score)
    
    return metrics_dict


def nested_k_fold_CV(X, y, k, n, clf_list, metric, shuffle=True, random_state=None):
    '''
    Perform n k-fold cross validations for each classfier in clf_list.
    Return a matrix with a metric of each validation.
    Each row of the matrix corresponds to a different classifier.
    The metrics arg value must be one of these:
        - los_loss
        - accuracy
        - roc_auc
    '''

    metric_array = np.zeros((len(clf_list), n))

    for i in xrange(len(clf_list)):
        for j in xrange(n):
            score, yhat = k_fold_cross_validation(X, y, k, clf_list[i], shuffle=shuffle,
                random_state=random_state)
            m = get_metrics(y, score, yhat)
            metric_array[i, j] = m[metric]
    
    return metric_array


def feature_selector(train, indep_variables, result, clf, k=5, n=5, min_gain=1e-03):
    '''
    Perform forward feature selection in order to maximize ROC AUC score.
    '''

    features_to_test = indep_variables[:]
    selected_feats = []
    best_metric = 0.5
    yt = np.array(train[result])
    print 'Feature selection algorithm\n{}'.format('-'*80)

    while len(features_to_test) > 0:
        d = {}

        for f in features_to_test:
            X = train[[f] + selected_feats].as_matrix().astype(float)
            m_array = nested_k_fold_CV(X, yt, k, n, [clf], 'roc_auc')
            d[f] = m_array.mean()
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
    print 'Feature selection is over.\n{}'.format('-'*80)

    return selected_feats
