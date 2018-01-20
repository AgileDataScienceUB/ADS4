import numpy as np
import pandas as pd

def generate_plotsB_files(test_data_path,pred):
    "Generates dict for each B plot. "

    df=pd.read_csv(test_data_path)
        
    dict_B1=plotB1(df,pred)
    dict_B2=plotB2(df,pred)
    dict_B3=plotB3(df,pred)
    dict_B4=plotB4(pred)
    dict_B5=plotB5(df,pred)
    
    return (dict_B1,dict_B2,dict_B3,dict_B4,dict_B5)

def plotB1(df,pred):
    "Returns path of a txt file with info about Scatter plot. "
    "First row contains strings with title and layers X and Y(seperated by comas). Then each row is a point (x,y) of a scatter plot"
    
    n=df.shape[0]
    title= "Probability to leave vs salary"
    
    salary_lavel= "MonthlyIncome" ##!!
    
    layerX= "Salary"
    layerY= "Probability to leave "
    x=df[salary_lavel].values
    dict = {"plot-name": title}
    dict["layer-x"]=layerX; dict["layer-y"]=layerY;
    dict["values"]=[x.tolist(),pred.tolist()]
    return(dict)

def plotB2(df,pred):
    "Returns path of a txt file with info about Column plot. "
    "First row contains strings with title and layers X and Y(seperated by comas)."
    "Then each row contains a string with the name of the column and its columns lenght y value"
    
    ##!!
    job_role_lavel= "JobRole"
    ##!!
    
    title="Probability of leaving respect job roles"
    layerX= "Job role"
    layerY= "Mean by role of lenght of service"
    dict = {"plot-name": title}
    dict["layer-x"]=layerX; dict["layer-y"]=layerY

    roles=df[job_role_lavel].values
    unique_roles=np.unique(roles)
    Ro=[]; Y=[]

    for i in unique_roles:
        inx= i==roles
        y=np.mean(pred[inx])
        Y.append(y); Ro.append(i)
    dict["values"]=[Ro,Y]
    return(dict)

def plotB3(df,pred):
    "Returns path of a txt file with info about Column plot. "
    "First row contains strings with title and layers X and Y(seperated by comas)."
    "Then each row contains a string with the name of the column and its columns lenght y value"
    
    ##!!
    age_lavel= "Age"
    ##!!
    
    title="Probability of leaving respect age group"
    layerX= "Age group"
    layerY= "Percentatge of employees with prediction higher than 80%"
    layersX=["Young(<30)", "Medium(30-50)","Old(>50)"]
   
    dict = {"plot-name": title}
    dict["layer-x"]=layerX; dict["layer-y"]=layerY   
    ages=df[age_lavel].values
    y=np.empty(3)
    
    ind= ages<30
    n=sum(ind); x=sum(pred[ind]>0.8) 
    y[0]=100*x/n
    
    ind= (ages>30) & (ages<50)
    n=sum(ind); x=sum(pred[ind]>0.8) 
    y[1]=100*x/n
    
    ind= ages>50
    n=sum(ind); x=sum(pred[ind]>0.8) 
    y[2]=100*x/n

    dict["values"]=[layersX,y.tolist()]
    return(dict)

def plotB4(pred):
    "Returns path of a txt file with info about Column plot(histrogram). "
    "First row contains strings with title and layers X and Y(seperated by comas)."
    "Then each row is a point (x,y) of a column plot"
        
    title="Histogram of probabiliy of leaving"
    layerX= "Proabability values"
    layerY= "Number of predicted probabilities"
    y,x=np.histogram(pred,bins=20)
    
    dict = {"plot-name": title}
    dict["layer-x"]=layerX; dict["layer-y"]=layerY
    dict["values"]=[y.tolist(),x.tolist()]
    
    return(dict)

def plotB5(df,pred):
    "Returns path of a txt file with info about Line plot. "
    "First row contains strings with title and layers X and Y(seperated by comas)."
    "Then each row contains a string with the name of the column and its columns lenght y value"
    
    ##!!
    LOS_lavel= "YearsAtCompany"
    ##!!
    
    title="Probability of leaving vs lenght of service"
    layerX= "Lenght of service (years)"
    layerY= "Probability of leaving"
   
    dict = {"plot-name": title}
    dict["layer-x"]=layerX; dict["layer-y"]=layerY
    values=[]
    LOS=df[LOS_lavel].values
    Dom=LOS.max()-LOS.min()  #domain
    num_points=30; I=Dom/num_points
    X=[]; Y=[]
    for i in range(num_points):
        ind= np.where( (i*I<=LOS) & (LOS<(i+1)*I),1,0)
        y=pred[ind].mean()
        if (sum(ind>0)):
            X.append((i+0.5)*I)
            Y.append(y) 
    dict["values"]=[X,Y]
    return(dict)

