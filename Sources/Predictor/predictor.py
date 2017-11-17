import random
import time
import zerorpc

import numpy as np
import pandas as pd 

from sklearn import model_selection
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

def clean_df(path,attrition=True):
    "given the path of a cvs file returns an enriched and cleaned dataset. If 'Attrition' it True retuns (X,y) where y is the target of the model  If false returns X "
    df = pd.read_csv(path)
    col_names = df.columns.tolist()
    to_drop=[]
    col_Onehot=[]
    col_other=[]
    for i in col_names:
            y=np.unique(df[i]) 
            x=y.shape[0]  
            if(x==1): #only one unique value--> we drop it
                to_drop.append(i)
            if(x==2 and type(y[0])==str): #--bolean--> 1 or 0 , we want that yes be 1, no be 0(do we?) this is poor. (solution: sort)
                if (y[0]=='Yes' or y[0]=='No'):
                    df[i]= np.where(df[i]=='Yes',1.,0.)
                else:
                    df[i]= np.where(df[i]==y[0],1.,0.)
            if(x>2 and x<30 and type(y[0])==str):  ##nomes miro tipus primer element si comences am numero i despres strings--> problemes
                col_Onehot.append(i)
            if(x >29 and type(y[0])==str): #we may use different techniques that onehot if we have a lot of values
                col_other.append(i) 
    df= df.drop(to_drop,axis=1)
    dummies = pd.get_dummies(df[col_Onehot])
    df[dummies.columns]=dummies
    df=df.drop(col_Onehot,axis=1)
    if(attrition==True):
        y=df['Attrition']  
        df=df.drop(['Attrition'],axis=1)
        X=df.as_matrix().astype(np.float)
        return (X,y)
    else:
        return df.as_matrix().astype(np.float)

def choose_model(X_train,X_test,y_train,y_test):
    #LR_par,LR_acc,LR_AreaROC=choose_Linear_regressor(X_train,X_test,y_train,y_test) ##model 0
    LR_par=0; LR_AreaROC =0.5
    Forest_par,Forest_acc,Forest_AreaROC = choose_random_forest_nestimators(X_train,X_test,y_train,y_test) ##model 1
    ##model 2,model3....
    AreaROC=[LR_AreaROC,Forest_acc]
    parameters=[LR_par,Forest_par]
    model=np.argmax(AreaROC)
    return (model, parameters[model])

def choose_random_forest_nestimators(X_train,X_test,y_train,y_test):
    "Returns N such that RandomForest with N estimators get maximum Accuracy"
    N=0
    Areamax=0
    MaxAcc=0
    for i in range(2,30,2):
        clf = RandomForestClassifier(n_estimators = i)
        clf.fit(X_train,y_train)
        yhat = clf.predict(X_test)
        score = clf.predict_proba(X_test)
        acc=metrics.accuracy_score(yhat,y_test)
        fpr, tpr,_ = metrics.roc_curve(y_test,score[:,1])
        if metrics.auc(fpr,tpr)>Areamax: #we choose the one when bigger area ROC
        #if acc > MaxAcc:                #we choose the one with bigger acc
            N=i
            Areamax=metrics.auc(fpr,tpr)
            MaxAcc=acc
    return(N,acc,Areamax)

class RandomPredictor:
    @staticmethod
    def predict():
        time.sleep(2)
        return random.choice([True, False])

class RandomForestPredictor:
    def __init__(self):
        self.dataset_path = 'dataset.csv'
        X,y = clean_df(path)
        X_train,X_test,y_train,y_test = model_selection.train_test_split(X,y,train_size=0.8,random_state=42)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train) ##scale the variables in the same range
        X_test = scaler.transform(X_test)
        self.model, self.parameters = choose_model(X_train,X_test,y_train,y_test)
    @staticmethod
    def predict():
        pass

class Predictor(object):
    def predict(self, data):
        return RandomPredictor.predict()

print("The Predictor is running...")
predictor_server = zerorpc.Server(Predictor())
predictor_server.bind("tcp://0.0.0.0:4242")
predictor_server.run()