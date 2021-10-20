# -*- coding: utf-8 -*-

"""
Created on Thu Oct  7 11:51:35 2021

@author: Hamzah
"""


def hybrid_forecasting(date):
    from sarima import time_series_pred
    from rf import rf_pred
    from data_rf_ext import data_ext
    from datetime import datetime
    
    import matplotlib.pyplot as plt
    #forecast_day='15-04-2020 00:00:00'
    forecast_day=date
    rf_val,rf_test=rf_pred(date)
    
    ts_val,ts_test=time_series_pred(forecast_day)
    date=datetime.strptime(forecast_day,'%d-%m-%Y %H:%M:%S')
    x=data_ext(date)
    
    train_data=x[0]
    val_data=x[1]
    rest_data=x[2]
    
    val_data['rf_predictions']=rf_val
    val_data['ts_predictions']=ts_val
    
    validations_df=val_data[['Date','rf_predictions','ts_predictions','Ghi']]
    from sklearn.ensemble import RandomForestRegressor
    
    X=validations_df[['rf_predictions','ts_predictions']]
    Y=validations_df[['Ghi']]
    model = RandomForestRegressor()
    model.fit(X, Y)
    importance = model.feature_importances_
    rf_weight=importance[0]
    ts_weight=importance[1]
    
    final_prediction=rest_data.copy()
    final_prediction['Random Forest forecasting']=rf_test
    final_prediction['SARIMAX forecasting']=ts_test
    final_prediction['Hybrid forecasting']=ts_weight*ts_test+rf_weight*rf_test
    final_prediction=final_prediction[['Date','Random Forest forecasting','SARIMAX forecasting','Hybrid forecasting','Ghi']]
    final_prediction=final_prediction.set_index('Date')
    #final_prediction.plot()
    return final_prediction
