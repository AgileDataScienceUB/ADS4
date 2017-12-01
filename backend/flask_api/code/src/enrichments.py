import pandas as pd
import numpy as np

def job_title_enrichment(df, job_title):

    if job_title:

        job_title2 = 'job_title2'
        job_title3 = 'job_title3'
        titles2 = [
            'analyst', 'clerk', 'director', 'exec assistant', 'manager',
        ]
        titles3 = [
            'accounting', 'accounts', 'audit', 'baker', 'compensation', 'dairy', 'finance',
            'human resources', 'investment', 'labor relations', 'legal counsel', 'meat', 'produce',
            'recruit', 'store', 'train',
        ]

        df[job_title2] = df[job_title].str.lower()
        df[job_title3] = df[job_title].str.lower()

        for t in titles2:
            df.loc[df[job_title2].str.contains(t), job_title2] = t
        for t in titles3:
            df.loc[df[job_title3].str.contains(t), job_title3] = t

        #print '(!) Job title enrichment has been performed.\n'


def length_of_service_enrichment(df, hire_date, record_date, length_of_service):
    if hire_date and record_date:
        df[length_of_service] = df[record_date].subtract(df[hire_date]).dt.days
        #print '(!) Length of service enrichment has been performed.\n'

    else:
        if length_of_service:
            if df[length_of_service].dtype == '<m8[ns]':
                df[length_of_service] = df[length_of_service].dt.day

def birth_date_enrichment(df, age, record_date, birth_date):
    df[birth_date] = df[record_date].subtract(pd.to_timedelta(df[age], unit='y'))
    #print '(!) Birth date enrichment has been performed.\n'


def birth_year_enrichment(df, birth_date, birth_year):
    df[birth_year] = df[birth_date].dt.year
    #print '(!) Birth year enrichment has been performed.\n'


def generation_enrichment(df, birth_year, age):
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
        #print '(!) Generation enrichment has been performed.\n'
