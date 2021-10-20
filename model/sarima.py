# -*- coding: utf-8 -*-

def time_series_pred(date):
    import pandas as pd
    from datetime import datetime
    import numpy as np
    from data_ext import data_ext
    from statsmodels.graphics.tsaplots import plot_pacf
    from statsmodels.graphics.tsaplots import plot_acf
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    
    date=datetime.strptime(date,'%d-%m-%Y %H:%M:%S')
    x=data_ext(date)
    p=1
    q=1
    d=1
    P=1
    D=1
    Q=1
    train_data=x[0]
    val_data=x[1]
    rest_data=x[2]
    #val_data['Irradiance'].plot()
   
    
    
    best_model = SARIMAX(train_data['Irradiance'], order=(p,d,q), seasonal_order=(P, D, Q, 24), 
                                  enforce_stationarity=False, enforce_invertibility=False).fit()
    
    print(best_model.summary())
    best_model.plot_diagnostics(figsize=(15,12))
    forecast_data = best_model.predict(241, 312)
    test_pred = best_model.predict(313, 336)

    return np.array(forecast_data),np.array(test_pred)

