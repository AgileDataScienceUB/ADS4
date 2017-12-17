import numpy as np
import pandas as pd
import os, errno

def generate_plotsA_files(train_data_path):
    "Generates a directory ./PlotsA with one txt file for each A plot. "
    try:
        os.makedirs("./PlotsA")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    df=pd.read_csv(train_data_path)
    pathA1=plotA1(df)
    pathA2=plotA2(df)
    pathA3=plotA3(df)
    pathA4=plotA4(df)
    return (pathA1,pathA2,pathA3,pathA4)
       
def plotA1(df):
    "Returns path of a txt file with info about a Pie Plot"
    "First row contains title, then each line contains a layer and a percentage of a Pie Plot"
    
    
    age_lavel="age" ## lavel with feature name of ages. it may be different!!
    
    
    title="Employees Ages"
    layersX=["Young(<30)", "Medium(30-50)","Old(>50)"]
    ages=np.empty(3)
    n=df.shape[0]
    ages[0]=sum(df[age_lavel]<=30)/n
    ages[1]=sum(df[age_lavel]<=50)/n -ages[0]
    ages[2]=sum(df[age_lavel]>50)/n
    file=open('./PlotsA/plotA1.txt','w')
    file.write('{} \n'.format(title))
    for i in range(3):
        file.write('{} {}\n'.format(layersX[i],ages[i]))
    file.close()
    return('./PlotsA/plotA1.txt')

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
    file=open('./PlotsA/plotA2.txt','w')
    file.write('{}, {}, {} \n'.format(title, layerX, layerY))
    for i in range(len(y)):  
        if(x[i]<0):
            x[i]=0
        file.write('{} {} \n'.format(x[i], y[i]))
    file.close()
    return('./PlotsA/plotA2.txt')
    
def plotA3(df):
    "Returns path of a txt file with info about Scatter plot. "
    "First row contains strings with title and layers X and Y(seperated by comas). Then each row is a point (x,y) of a scatter plot"
    
    salary_lavel= "MonthlyIncome" ##!!
    lenght_service_lavel="length_of_service"
    
    
    n=df.shape[0]
    title= "Salary vs lenght of service"
    layerX= "Salary"
    layerY= "Lenght of service"
    x=df[salary_lavel].values
    y=df[lenght_service_lavel].values
    file=open('./PlotsA/plotA3.txt','w')
    file.write('{}, {}, {} \n'.format(title, layerX, layerY))
    for i in range(n):     
        file.write('{} {} \n'.format(x[i], y[i]))
    file.close()
    return('./PlotsA/plotA3.txt')

def plotA4(df):
    "Returns path of a txt file with info about Column plot. "
    "First row contains strings with title and layers X and Y(seperated by comas)."
    "Then each row contains a string with the name of the column and its columns lenght y value"
    
    lenght_service_lavel="length_of_service" ##!!
    job_role_lavel= "BUSINESS_UNIT"
    
    title="Lenght of service by job roles"
    layerX= "Job role"
    layerY= "Mean by role of lenght of service"
    file=open('./PlotsA/plotA4.txt','w')
    file.write('{}, {}, {} \n'.format(title, layerX, layerY))    
    X=df[lenght_service_lavel].values
    roles=df[job_role_lavel].values
    unique_roles=np.unique(roles)
    for i in unique_roles:
        inx= i==roles
        y=np.mean(X[inx])
        file.write('{} {} \n'.format(i, y))
    file.close()
    return('./PlotsA/plotA4.txt')
