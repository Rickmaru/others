#author;R.Kunimoto, TAKENAKA co.
#coding:utf-8

import random
from sklearn import preprocessing
from sklearn import ensemble
from sklearn import svm
from sklearn import linear_model
from sklearn import neural_network
import pandas as pd
import numpy as np
import warnings
import sklearn
warnings.filterwarnings('ignore')

def checker(list,id):
    for ai in list:
        if ai == id:
            return True
        else:
            continue
    return False

path = 'C:\\Users\\1500570\\Documents\\R\\WS\\kosugi\\'
data = pd.read_csv(path+"data.csv")
# data = data.sample(3000)

y = data["yyy"]
x = data[["week_sin","week_cos","time_sin","time_cos","sunlight","temp","moist","y1"]]

score = []
n_ml = 0

while n_ml < 1:
    n_term = 0
    while n_term < 3:
        n_node = 0
        score2 = []
        while n_node < 4:
            aarray = []
            parray = []
            i_list=[]
            j = 0
            rmse = 0
            t = 14*(n_term+1)
            term = t*48 -1
            while j < 1000:
                flag = False
                while flag == False:
                    i = random.randint(1,len(data)-term-2)
                    if checker(i_list,i) == True:
                        continue
                    else:
                        flag = True
                        i_list.append(i)
                if n_ml == 2:
                    namae = "rfr"
                    rf = ensemble.RandomForestRegressor(n_estimators=10)
                elif n_ml == 2:
                    namae = "svr"
                    rf = svm.SVR()
                elif n_ml == 2:
                    namae = "lmr"
                    rf = linear_model.LinearRegression()
                elif n_ml == 0:
                    namae = "nnr"
                    rf = neural_network.MLPRegressor(hidden_layer_sizes=(3*(n_node+1),1))
                x_train = x.iloc[i:i+term,:]
                y_train = y.iloc[i:i+term]
                x_test = x.iloc[i+term,:]
                y_test = y.iloc[i+term]
                rf.fit(x_train,y_train)
                py = rf.predict(x_test)
                aarray.append(y_test)
                parray.append(float(py))
                rmse += (y_test-float(py))**2
                j += 1
                if(j%100 == 0):
                    print("i = "+str(j))
            p = np.vstack((aarray,parray))
            p = p.swapaxes(0,1)
            np.savetxt(path+"written_"+namae+"_"+str((n_term+1)*14)+"_"+str((n_node+1)*3)+".csv",p,delimiter=",")
            n_node += 1
            score2.append(float(rmse/float(1000)))
            print(score2)
            print(namae+str(n_term)+str(n_node)+" is end")
        score.append(score2)
        n_term += 1
    n_ml += 1

print(score)
print("end")
