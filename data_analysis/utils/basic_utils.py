# Imports
import numbers

import pandas as pd
import numpy as np
import datetime as dt

from IPython.display import display


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
