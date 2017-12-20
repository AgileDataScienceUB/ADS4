
import pandas as pd
import numpy as np
import datetime as dt

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn import metrics

from basic_utils import is_categorical, is_continuous, is_datetime
from ml_utils import (k_fold_cross_validation, get_metrics, feature_selector, split_dataset,
    get_X_and_y)
from enrichments import (job_title_enrichment, length_of_service_enrichment, birth_year_enrichment,
    birth_date_enrichment, generation_enrichment)
from feature_engineering import get_woe_series, get_woe_dict


def create_predictor(file_name, target, employee_id=None, record_id=None, hire_date=None,
                     record_date=None, termination_date=None, length_of_service=None,
                     age=None, birth_date=None, birth_year=None, other_target_fields=[],
                     job_title=None, special_field_types={}):
    '''
    Enriches the dataset and transform its features.
    Performs a forward feature selection algorithm.
    Fit a classifier with the selected features.
    Validates the classifier with a validation set.

    Return:
        - Selected features list
        - WOE dictionaries for categorical features
        - Fitted classifier
        - Fitted scaler
        - Validation metrics
    '''

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
        birth_year: float
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

    # Enrichments

    job_title_enrichment(df, job_title)

    if hire_date and record_date:
        length_of_service = 'length_of_service'
        length_of_service_enrichment(df, hire_date, record_date, length_of_service)

    if age and record_date and not birth_date:
        birth_date = 'birth_date'
        birth_date_enrichment(df, age, record_date, birth_date)

    if birth_date and not birth_year:
        birth_year = 'birth_year'
        birth_year_enrichment(df, birth_date, birth_year)

    generation_enrichment(df, birth_year, age)

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
        if is_categorical(df, c):
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
                # One hot encoder (TO DO)
                pass

        # Continuous features
        elif is_continuous(df, c):
            # Outliers detection (TO DO)
            # Missing values imputation (TO DO)
            pass

    indep_variables = []
    for c in df.columns:
        if c not in excluded_features and not is_datetime(df, c):
            indep_variables.append(c)

    # Split train and validation set
    train, valid = split_dataset(df, sorting_field=record_date, test_size=0.2)

    # Weight of evidence for the train set
    for c in [v for v in indep_variables if is_categorical(train, v)]:
        d = get_woe_dict(train, result, c)
        train[c] = get_woe_series(train, c, d)
        valid[c] = get_woe_series(valid, c, d)

    # Define the classifier
    clf = LogisticRegression()

    # Feature selection
    selected_feats = feature_selector(train, indep_variables, result, clf)
    assert selected_feats, 'The feature selector has excluded all independent variables.'

    # Grid search (TO DO)

    # Predict validation set

    Xt, yt = get_X_and_y(train, selected_feats, result)
    Xv, yv = get_X_and_y(valid, selected_feats, result)

    scaler = StandardScaler()
    Xt_scaled = scaler.fit_transform(Xt)
    clf.fit(Xt_scaled, yt)

    Xv_scaled = scaler.transform(Xv)
    score = clf.predict_proba(Xv_scaled)[:,1]
    yhat = clf.predict(Xv_scaled)
    valid_metrics = get_metrics(yv, score, yhat)

    fpr, tpr, _ = metrics.roc_curve(yv, score)

    dict_A5 = {
        "results": [
            {
                "param": "False positive rate",
                "val": list(fpr)
            },
            {
                "param": "True positive rate",
                "val": list(tpr)
            }
        ]
    }

    # Weight of evidence for the whole dataframe
    woe_dicts = {}
    for c in [v for v in indep_variables if is_categorical(df, v)]:
        d = get_woe_dict(df, result, c)
        df[c] = get_woe_series(df, c, d)
        woe_dicts[c] = d

    # Fit the classifier with the whole dataframe
    X, y = get_X_and_y(df, selected_feats, result)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    clf.fit(X_scaled, y)

    return selected_feats, woe_dicts, clf, scaler, valid_metrics, dict_A5


def get_prediction(file_name, selected_feats, woe_dicts, clf, scaler, employee_id=None,
                   record_id=None, hire_date=None, record_date=None, termination_date=None,
                   length_of_service=None, age=None, birth_date=None, birth_year=None,
                   other_target_fields=[], job_title=None, special_field_types={}):
    '''
    Enriches the dataset and transform its features.
    Return:
        - Score (predict_proba)
        - Prediction (predict)
        - Dataframe
    '''

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
        birth_year: float
    }
    field_types.update(special_field_types)

    # Load dataset
    df = pd.read_csv(file_name, dtype=field_types, parse_dates=date_fields)

    # Enrichments
    job_title_enrichment(df, job_title)

    if hire_date and record_date:
        length_of_service = 'length_of_service'
        length_of_service_enrichment(df, hire_date, record_date, length_of_service)

    if age and record_date and not birth_date:
        birth_date = 'birth_date'
        birth_date_enrichment(df, age, record_date, birth_date)

    if birth_date and not birth_year:
        birth_year = 'birth_year'
        birth_year_enrichment(df, birth_date, birth_year)

    generation_enrichment(df, birth_year, age)

    # Weight of evidence for the whole dataframe
    for c in [v for v in selected_feats if is_categorical(df, v)]:
        d = woe_dicts[c]
        df[c] = get_woe_series(df, c, d)

    X = df[selected_feats].as_matrix().astype(float)
    X_scaled = scaler.fit_transform(X)
    score = clf.predict_proba(X_scaled)[:, 1]
    y_hat = clf.predict(X_scaled)

    result = pd.DataFrame({
        employee_id: df[employee_id],
        'score': score
    })

    return score, result
