import numpy as np
import pandas as pd
import os, errno
import pickle as pk

def generate_plotsB_files(test_data_path,predictions_path):
    "Generates a directory ./PlotsB with one txt file for each B plot. "
    try:
        os.makedirs("./PlotsB")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    df=pd.read_csv(test_data_path)
    pred=pk.load( open( predictions_path, "rb" ) ) ###pred has to be an array with the predictions ### FALTA TEST NIDEA d'on es fa aquest pickle ni on es guarda
    
    pathB1=plotB1(df,pred)
    pathB2=plotB2(df,pred)
    pathB3=plotB3(df,pred)
    pathB4=plotB4(pred)
    pathB5=plotB5(df,pred)
    
    return (pathB1,pathB2,pathB3,pathB4,pathB5)

def plotB1(df,pred):
    "Returns path of a txt file with info about Scatter plot. "
    "First row contains strings with title and layers X and Y(seperated by comas). Then each row is a point (x,y) of a scatter plot"
    
    n=df.shape[0]
    title= "Probability to leave vs lenght of service"
    
    salary_lavel= "MonthlyIncome" ##!!
    
    layerX= "Salary"
    layerY= "Probability to leave "
    x=df[salary_lavel].values

    file=open('./PlotsB/plotB1.txt','w')
    file.write('{}, {}, {} \n'.format(title, layerX, layerY))
    for i in range(n):     
        file.write('{} {} \n'.format(x[i], pred[i]))
    file.close()
    return('./PlotsB/plotB1.txt')

def plotB2(df,pred):
    "Returns path of a txt file with info about Column plot. "
    "First row contains strings with title and layers X and Y(seperated by comas)."
    "Then each row contains a string with the name of the column and its columns lenght y value"
    
    ##!!
    job_role_lavel= "BUSINESS_UNIT"
    ##!!
    
    title="Probability of leaving respect job roles"
    layerX= "Job role"
    layerY= "Mean by role of lenght of service"
    file=open('./PlotsB/plotB2.txt','w')
    file.write('{}, {}, {} \n'.format(title, layerX, layerY))    

    roles=df[job_role_lavel].values
    unique_roles=np.unique(roles)
    for i in unique_roles:
        inx= i==roles
        y=np.mean(pred[inx])
        file.write('{} {} \n'.format(i, y))
    file.close()
    return('./PlotsB/plotB2.txt')

def plotB3(df,pred):
    "Returns path of a txt file with info about Column plot. "
    "First row contains strings with title and layers X and Y(seperated by comas)."
    "Then each row contains a string with the name of the column and its columns lenght y value"
    
    ##!!
    age_lavel= "age"
    ##!!
    
    title="Probability of leaving respect age"
    layerX= "Age group"
    layerY= "Predicted mean by age group"
    layersX=["Young(<30)", "Medium(30-50)","Old(>50)"]
   
    file=open('./PlotsB/plotB3.txt','w')
    file.write('{}, {}, {} \n'.format(title, layerX, layerY))    
    ages=df[age_lavel].values
    y=np.empty(3)
    
    ind= ages<30
    n=sum(ind); x=sum(pred[ind]>0.8) 
    y[0]=x/n
    
    ind= (ages>30) & (ages<50)
    n=sum(ind); x=sum(pred[ind]>0.8) 
    y[1]=x/n
    
    ind= ages>50
    n=sum(ind); x=sum(pred[ind]>0.8) 
    y[2]=x/n
    
    for i in range(3) :        
        file.write('{} {}\n'.format(layersX[i],y[i]))
    file.close()
    return('./PlotsB/plotB3.txt')

def plotB4(pred):
    "Returns path of a txt file with info about Column plot(histrogram). "
    "First row contains strings with title and layers X and Y(seperated by comas)."
    "Then each row is a point (x,y) of a column plot"
        
    title="Histogram of probabiliy of leaving"
    layerX= "Proabability values"
    layerY= "Number of predicted probabilities"
    y,x=np.histogram(pred,bins=20)
    file=open('./PlotsB/plotB4.txt','w')
    file.write('{}, {}, {} \n'.format(title, layerX, layerY))
    for i in range(len(y)):  
        file.write('{} {} \n'.format(x[i], y[i]))
    file.close()
    return('./PlotsB/plotB4.txt')

def plotB5(df,pred):
    "Returns path of a txt file with info about Line plot. "
    "First row contains strings with title and layers X and Y(seperated by comas)."
    "Then each row contains a string with the name of the column and its columns lenght y value"
    
    ##!!
    LOS_lavel= "length_of_service"
    ##!!
    
    title="Probability of leaving respect age group"
    layerX= "Lenght of service"
    layerY= "Probability of leaving"
   
    file=open('./PlotsB/plotB5.txt','w')
    file.write('{}, {}, {} \n'.format(title, layerX, layerY))   
    
    LOS=df[LOS_lavel].values
    Dom=LOS.max()-LOS.min()  #domain
    num_points=30; I=Dom/num_points

    for i in range(num_points):
        ind= np.where( (i*I<=LOS) & (LOS<(i+1)*I),1,0)
        y=pred[ind].mean()
        if (sum(ind>0)):
            file.write('{} {}\n'.format((i+0.5)*I,y))
    
    file.close()
    return('./PlotsB/plotB5.txt')

