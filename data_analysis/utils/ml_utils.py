# Imports
import numpy as np

from sklearn import cross_validation
from sklearn import metrics
from sklearn.preprocessing import StandardScaler


def k_fold_cross_validation(X, y, k, clf, shuffle=True, random_state=None):
    
    # Determine the indices for each fold
    cv = cross_validation.KFold(X.shape[0], n_folds=k, shuffle=shuffle, random_state=random_state)
    
    # Initialize the score and yhat array
    score = np.zeros((X.shape[0],1))
    yhat = np.zeros((X.shape[0],1))
    
    # Cross validation
    for train_idx, test_idx in cv:
        X_train,y_train = X[train_idx,:], y[train_idx]
        X_test,y_test = X[test_idx,:], y[test_idx]

        scaler = StandardScaler()
        X_train_scaled=scaler.fit_transform(X_train)

        clf.fit(X_train_scaled,y_train)

        X_test_scaled = scaler.transform(X_test)

        score[test_idx] = clf.predict_proba(X_test_scaled)[:, 1].reshape(-1,1)
        yhat[test_idx] = clf.predict(X_test_scaled).reshape(-1,1)

    return score, yhat


def nested_k_fold_CV(X, y, k, n, clf_list, metric, shuffle=True, 
    random_state=None):
        
    # Initializing metric array
    metric_array = np.zeros((n, len(clf_list)))

    for i in xrange(len(clf_list)):

        for j in xrange(n):

            # K-fold cross validation
            score, yhat = k_fold_cross_validation(X, y, k, clf_list[i], 
                shuffle=shuffle, random_state=random_state)

            # Get metrics
            m = get_metrics(y, score, yhat)
            metric_array[j, i] = m[metric]
    
    return metric_array


def get_metrics(y, score, yhat):
    
    # Create a metrics dict
    metrics_dict = {}
    
    # Log loss
    metrics_dict['log_loss'] = metrics.log_loss(y, score)

    # Accuracy
    metrics_dict['accuracy'] = metrics.accuracy_score(y, yhat)

    # ROC AUC
    fpr, tpr, _ = metrics.roc_curve(y, score)
    metrics_dict['roc_auc'] = metrics.auc(fpr, tpr)
    
    return metrics_dict

