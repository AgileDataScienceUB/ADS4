# This file contains different types of aggregations for the different types of
#  plots

import numpy as np
import pandas as pd

def generate_plotsA_dict(train_data_path):
    "Generates a directory ./PlotsA with one txt file for each A plot. "
    df=pd.read_csv(train_data_path)
    dict_A1=plotA1(df)
    dict_A2=plotA2(df)
    dict_A3=plotA3(df)
    dict_A4=plotA4(df)
    return (dict_A1,dict_A2,dict_A3,dict_A4)

def plotA1(df):
    "Returns path of a txt file with info about a Pie Plot"
    "First row contains title, then each line contains a layer and a percentage of a Pie Plot"

    age_lavel="Age" ## lavel with feature name of ages. it may be different depending on dataset!!

    title="Employees Ages"

    layersX=["Young(<30)", "Medium(30-50)","Old(>50)"]
    ages=np.empty(3)
    n=df.shape[0]
    ages[0]=sum(df[age_lavel]<=30)/n
    ages[1]=sum(df[age_lavel]<=50)/n -ages[0]
    ages[2]=sum(df[age_lavel]>50)/n
    dict = {"plot-name": title}
    dict["values"]=[layersX,ages]
    return(dict)

def plotA2(df):
    "Returns path of a txt file with info about Column plot(histrogram). "
    "First row contains strings with title and layers X and Y(seperated by comas)."
    "Then each row is a point (x,y) of a column plot"

    salary_lavel= "MonthlyIncome" ##!!

    title="Histogram of Salaries"
    layerX= "Salary"
    layerY= "Number of employees"
    X=df[salary_lavel].values
    y,x=np.histogram(X,bins=20)
    dict = {"plot-name": title}
    dict["layer-x"]=layerX; dict["layer-y"]=layerY;
    for i in range(len(x)):
        if(x[i]<0):
            x[i]=0
    dict["values"]=[x.tolist(),y.tolist()]
    return(dict)

def plotA3(df):
    "Returns path of a txt file with info about Scatter plot. "
    "First row contains strings with title and layers X and Y(seperated by comas). Then each row is a point (x,y) of a scatter plot"

    salary_lavel= "MonthlyIncome" ##!!
    lenght_service_lavel="YearsAtCompany"

    n=df.shape[0]
    title= "Salary vs lenght of service"
    layerX= "Salary"
    layerY= "Lenght of service"
    x=df[salary_lavel].values
    y=df[lenght_service_lavel].values
    dict = {"plot-name": title}
    dict["layer-x"]=layerX; dict["layer-y"]=layerY;
    dict["values"]=[x.tolist(),y.tolist()]
    return(dict)

def plotA4(df):
    "Returns path of a txt file with info about Column plot. "
    "First row contains strings with title and layers X and Y(seperated by comas)."
    "Then each row contains a string with the name of the column and its columns lenght y value"

    lenght_service_lavel="YearsAtCompany" ##!!
    job_role_lavel= "JobRole"

    title="Lenght of service by job roles"
    layerX= "Job role"
    layerY= "Mean by role of lenght of service"
    dict = {"plot-name": title}
    dict["layer-x"]=layerX; dict["layer-y"]=layerY;

    X=df[lenght_service_lavel].values
    roles=df[job_role_lavel].values
    unique_roles=np.unique(roles)
    Ro=[];Y=[]
    for i in unique_roles:
        inx= i==roles
        y=np.mean(X[inx])
        Ro.append(i); Y.append(y)
    dict["values"]=[Ro,Y]
    return(dict)
