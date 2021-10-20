# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 05:47:13 2021

@author: Hamzah
"""


def rf_pred(date):
    from datetime import datetime
    import numpy as np
    from data_rf_ext import data_ext
    import pandas as pd
    import numpy as np
    from matplotlib import pyplot as plt
    import matplotlib 
    import os
    date=datetime.strptime(date,'%d-%m-%Y %H:%M:%S')
    x=data_ext(date)

    train_data=x[0]
    val_data=x[1]
    rest_data=x[2]
    #rest_data=np.asarray(rest_data['Ghi']).reshape(-1,1)
    X_train = np.asarray(train_data.iloc[:,1:13])
    #Best option is to take important features instead of all features
    val_pred = np.asarray(val_data.iloc[:,1:13])
    rest_pred = np.asarray(rest_data.iloc[:,1:13])
    
    Y_train= np.asarray(train_data.iloc[:,-1])
    from sklearn.ensemble import RandomForestRegressor
    rf = RandomForestRegressor(n_estimators = 100, random_state = 4)
    rf.fit(X_train, Y_train)
    
    predictions = rf.predict(val_pred)
    test_pred=rf.predict(rest_pred)
    return predictions,test_pred

