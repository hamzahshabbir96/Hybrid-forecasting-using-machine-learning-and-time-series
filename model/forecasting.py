# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 10:34:25 2021

@author: Hamzah
"""
date='17-01-2020 00:00:00'

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

train_data['Ghi'].plot()
val_data['Ghi'].plot()
rest_data['Ghi'].plot()


ts_val.plot()
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
final_prediction['Hybrid forecasting']=ts_weight*ts_test+rf_weight*rf_test

final_prediction=final_prediction[['Date','Random Forest forecasting','SARIMAX forecasting','Hybrid forecasting','Ghi']]
final_prediction=final_prediction.set_index('Date')
   
final_prediction.plot()
final_prediction=final_prediction.rename(columns={"Ghi":"Real forecasting"})

ax = final_prediction.plot(figsize=(10,7))#,marker='.',markersize=15)
ax.set_xlabel("Time",fontsize=18)
ax.set_ylabel("Global Horizontal Irradiance (W⋅m−2)",fontsize=18)
#ax.set_title('Forecasted irradiance from SARIMAX',fontsize=18);
plt.xticks(fontsize=15) 
plt.yticks(fontsize=15) 
plt.legend(loc=2, prop={'size':12})
plt.grid()
plt.savefig('16thjan.svg', dpi=600, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0,
        frameon=None, metadata=None)


pred=final_prediction.copy()
from hybrid import hybrid_forecasting
#pred=hybrid_forecasting(forecast_day)
#from sarima import ts_only
from sklearn.metrics import mean_squared_error
from math import sqrt
import numpy as np

Hybrid_forecast=[]
Error=[]
Time_series_forecast=[]
Random_forest_forecast=[]
#test_p=pred[pred['Ghi'] != 0]



rf_arr=pred['Random Forest forecasting'].tolist()
ts_arr=pred['SARIMAX forecasting'].tolist()
hybrid_arr=pred['Hybrid forecasting'].tolist()
real=pred['Real forecasting'].tolist()

'''...............MAE(mean absolute error).............'''
#Random forest
error_mae=[]
for i in range(0,24):
    error_mae.append(abs(real[i]-rf_arr[i]))
temp=[]
for i in error_mae:
    if i!=0:
        temp.append(i)
Random_forest_forecast.append((sum(temp)/len(temp)))
error_mae=[]
#Time series
for i in range(0,24):
    error_mae.append(abs(real[i]-ts_arr[i]))
temp=[]
for i in error_mae:
    if i!=0:
        temp.append(i)
Time_series_forecast.append((sum(temp)/len(temp)))
error_mae=[]
#hybrid
for i in range(0,24):
    error_mae.append(abs(real[i]-ts_arr[i]))
temp=[]
for i in error_mae:
    if i!=0:
        temp.append(i)
Hybrid_forecast.append((sum(temp)/len(temp)))
error_mae=[]

'''...............NMAE(Normalized Mean Absolute Error).............'''
#Random forest
error_nmae=[]
for i in range(0,24):
    error_nmae.append(abs(real[i]-rf_arr[i]))
temp=[]
for i in error_nmae:
    if i!=0:
        temp.append(i)
Random_forest_forecast.append((sum(temp)/(len(temp)*max(real)))*100)
error_nmae=[]
#Time series
for i in range(0,24):
    error_nmae.append(abs(real[i]-ts_arr[i]))
temp=[]
for i in error_nmae:
    if i!=0:
        temp.append(i)
Time_series_forecast.append((sum(temp)/(len(temp)*max(real)))*100)
error_nmae=[]
#hybrid
for i in range(0,24):
    error_nmae.append(abs(real[i]-hybrid_arr[i]))
temp=[]
for i in error_nmae:
    if i!=0:
        temp.append(i)
Hybrid_forecast.append((sum(temp)/(len(temp)*max(real)))*100)
error_nmae=[]
'''...............nRMSE(Normalized Root Mean Square Error ).............'''
#Random forest
error  =  (np.sqrt(np.mean(np.square((np.asarray(real)-np.asarray(rf_arr)) ))))
error = error*100/max(real)
Random_forest_forecast.append(error)
#Time series
error  =  (np.sqrt(np.mean(np.square((np.asarray(real)-np.asarray(ts_arr)) ))))
error = error*100/max(real)
Time_series_forecast.append(error)
#hybrid
error  =  (np.sqrt(np.mean(np.square((np.asarray(real)-np.asarray(hybrid_arr)) ))))
error = error*100/max(real)
Hybrid_forecast.append(error)

'''...............wMAE(Weighted mean absolute error).............'''
#Random forest
num  =  np.sum(abs(np.asarray(real)-np.asarray(rf_arr)) )
den=np.sum(np.asarray(real))
error = num*100/den
Random_forest_forecast.append(error)
#Time series
num  =  np.sum(abs(np.asarray(real)-np.asarray(ts_arr)) )
den=np.sum(np.asarray(real))
error = num*100/den
Time_series_forecast.append(error)
#Hybrid
num  =  np.sum(abs(np.asarray(real)-np.asarray(hybrid_arr)) )
den=np.sum(np.asarray(real))
error = num*100/den
Hybrid_forecast.append(error)
'''...............MAPE(Mean Absolute Percentage Error).............'''
#Random Forest
real_t=[]
rf_t=[]
for i in range(len(real)):
    if real[i] != 0:
        real_t.append(real[i])
        rf_t.append(rf_arr[i])
        
num  =  np.mean(np.sum(abs(np.asarray(real_t)-np.asarray(rf_t))/np.asarray(real_t)))
error = num*100
Random_forest_forecast.append(error)
#Time series
real_t=[]
rf_t=[]
for i in range(len(real)):
    if real[i] != 0:
        real_t.append(real[i])
        rf_t.append(ts_arr[i])
        
num  =  np.mean(np.sum(abs(np.asarray(real_t)-np.asarray(rf_t))/np.asarray(real_t)))
error = num*100
Time_series_forecast.append(error)
#Hybrid
real_t=[]
rf_t=[]
for i in range(len(real)):
    if real[i] != 0:
        real_t.append(real[i])
        rf_t.append(hybrid_arr[i])
        
num  =  np.mean(np.sum(abs(np.asarray(real_t)-np.asarray(rf_t))/np.asarray(real_t)))
error = num*100
Hybrid_forecast.append(error)
'''...............EWAE(Envelope Weighted absolute error).............'''
#Random Forest
den=[]
for i in range(len(real)):
    if real[i] > rf_arr[i]:
        den.append(real[i])
    else:
        den.append(rf_arr[i])
        
num  =  np.sum(abs(np.asarray(real)-np.asarray(rf_arr)))
den=np.sum(np.asarray(den))
error = num/den*100
Random_forest_forecast.append(error)
#Time series
den=[]
for i in range(len(real)):
    if real[i] > ts_arr[i]:
        den.append(real[i])
    else:
        den.append(rf_arr[i])
        
num  =  np.sum(abs(np.asarray(real)-np.asarray(ts_arr)))
den=np.sum(np.asarray(den))
error = num/den*100
Time_series_forecast.append(error)
#Hybrid
den=[]
for i in range(len(real)):
    if real[i] > hybrid_arr[i]:
        den.append(real[i])
    else:
        den.append(rf_arr[i])
        
num  =  np.sum(abs(np.asarray(real)-np.asarray(hybrid_arr)))
den=np.sum(np.asarray(den))
error = num/den*100
Hybrid_forecast.append(error)
#################################
import pandas as pd
error_name=['mean absolute error','Normalized Mean Absolute Error','Normalized Root Mean Square Error','Weighted mean absolute error','Mean Absolute Percentage Error','Envelope Weighted absolute error']
error_set = pd.DataFrame(list(zip(Random_forest_forecast,Time_series_forecast,Hybrid_forecast)), columns=['Random_forest_forecast','Time_series_forecast','Hybrid_forecast'])
error_set['Error name']=error_name
error_set=error_set.set_index('Error name')
error_set.to_excel('16th jan.xlsx',index=error_name)