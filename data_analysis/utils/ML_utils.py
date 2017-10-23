
# Imports
from __future__ import division

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

import math
import string
import numbers

from IPython.display import HTML
from IPython.display import display

from sklearn import feature_selection
from sklearn import cross_validation
from sklearn import metrics
from sklearn import grid_search
from sklearn import ensemble
from sklearn import linear_model
from sklearn import neighbors
from sklearn import svm
from sklearn.preprocessing import StandardScaler



####################################
## PILL1 - CRASH COURSE ON PYTHON ##
####################################

# A function in Python

def factorial(n):
    fact = 1L
    for factor in range(n,0,-1):
        fact = fact * factor
    return fact


def fib1(n):
    if n==1:
        return 1
    if n==0:
        return 0
    return fib1(n-1) + fib1(n-2)


def fib2(n):
    a, b = 0, 1
    for i in range(1,n+1):
        a, b = b, a + b
    return a


def gcd(a,b):   # Euclides algorithm v2.0: idiomatic Python
    while a:
        a, b = b%a, a
    return b


# Conditionals

def average(a):
    sum = 0.0
    for i in a:
        sum = sum + i
    return sum/len(a)


def sumdif(x,y):
    sum, dif = x+y, x-y
    return sum, dif


# References

def head(list):
    return list[0]


def change_first_element(list):
    list[0]=0


def tail(list):
    return list[1:]     # we are creating a new list


# Tuples

def compare((w1,c1),(w2,c2)):
# A sorting funtion returns negative if x<y, zero if x==y, positive if x>y.
    if c1 < c2:
        return -1
    elif c1 == c2:
        return 0
    else:
        return 1


# Lists (and dictionary) comprehensions

def res(n,b):
    bin_a = '.'
    for i in range(b):
        n *= 2
        bin_a +=  str(int(n))
        n = n % 1
    return bin_a


def binRep(n):
    while True:
        n *= 2
        yield int(n)
        n = n % 1


# Objects

class Rectangle:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    description = "This shape has not been described yet"
    author = "Nobody has claimed to make this shape yet"
    def area(self):
        return self.x * self.y
    def perimeter(self):
        return 2 * self.x + 2 * self.y
    def describe(self,text):
        self.description = text
    def authorName(self,text):
        self.author = text
    def scaleSize(self,scale):
        self.x = self.x * scale
        self.y = self.y * scale


# A basic CSV reader

def tryfloat(x):
    try:
        return float(x)
    except:
        return x
    
def isfloat(x):
    try:
        float(x)
        return True
    except:
        return False


def read_csv(filename, hasHeader=False):
    header = []
    data = []
    with open(filename) as fp:
        lines = fp.readlines()

        if hasHeader:
            header = lines[0].split(",")

        for line in lines[int(hasHeader):]:                
            data.append(map(tryfloat, line.split(",")))

    return header, data


def extract_column(data, column_index):
    return [l[column_index] for l in data]


class DataList(object):
    def __DataList__(self, datalist = []):
        self.data = datalist
        
        
    def read_csv(self, filename, has_header=False):
        self.header = []
        self.data = []
        with open(filename) as fp:
            lines = fp.readlines()

            if has_header:
                self.header = lines[0].split(",")

            for line in lines[int(has_header):]:                
                self.data.append(map(tryfloat, line.split(",")))

        return self
        
        
    def get_column(self, column):
        if not isfloat(column):
            column = self.header.index(column)

        return np.array([l[column] for l in self.data])

    
    def get_values(self):
        return np.array(self.data)


#############################################
## PILL2 - FIRST STEPS IN MACHINE LEARNING ##
#############################################

def accuracy(y, yhat):
    return (y == yhat).mean()


def majority_class_accuracy(y):
    y_mean = (y).mean()
    if y_mean > 0.5:
        return y_mean
    else:
        return 1 - y_mean


############
## OTHERS ##
############

def print_full(x, n=None, m=None):
    """
    Print a full pandas object.

    Args:
        x: dataframe or series
        n: max rows to show
        m: max columns to show
    """

    shape = x.shape
    pd.set_option('display.max_rows', n or shape[0])
    if (len(shape) > 1):
        pd.set_option('display.max_columns', m or shape[1])
    display(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')


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

# Check data types

BOOLEAN_TYPES = (bool, np.bool_)
DATE_TYPES = (np.datetime64, pd.Timestamp, dt.date)
CONTINUOUS_TYPES = (numbers.Real, ) + DATE_TYPES


def is_continuous_type(_type):
    """
    Return True if the given type looks like a continuous type.
    """
    return issubclass(_type, CONTINUOUS_TYPES)


def is_boolean_type(_type):
    """
    Return True if the given type looks like boolean type.
    """
    return issubclass(_type, BOOLEAN_TYPES)


def is_date_type(_type):
    """
    Return True if the given type looks like boolean type.
    """
    return issubclass(_type, DATE_TYPES)


def is_categorical_type(_type):
    """
    Return True if the given type looks like boolean type.
    """
    return not is_boolean_type(_type) and not is_continuous_type(_type)


def is_continuous(df, var):
    """
    Return True if the given variable looks like continuous variable.
    """
    return not isinstance(var, (list, tuple)) and is_continuous_type(df[var].dtype.type)


def is_boolean(df, var):
    """
    Return True if the given variable looks like boolean variable.
    """
    return not isinstance(var, (list, tuple)) and is_boolean_type(df[var].dtype.type)


def is_datetime(df, var):
    """
    Return True if the given variable looks like a datetime.
    """
    return not isinstance(var, (list, tuple)) and is_date_type(df[var].dtype.type)


def is_categorical(df, var):
    """
    Return True if the given variable looks like categorical variable.
    """
    return not is_continuous(df, var) and not is_boolean(df, var)