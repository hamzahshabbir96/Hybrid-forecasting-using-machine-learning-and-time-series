# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 05:45:45 2021

@author: Hamzah
"""
import pandas as pd
from datetime import timedelta
from datetime import datetime

#data_extraction
def data_ext(forecast_day,train_day=10,val_day=3,test_day=1):
    start_day=forecast_day-timedelta(14)
    end_train=forecast_day-timedelta(4)
    start_val=forecast_day-timedelta(4)
    end_val=forecast_day-timedelta(1)
    #date=datetime.strptime(forecast_day,'%d-%m-%Y %H:%M:%S')
    data=pd.read_excel("data1.xlsx")
    #data=data[data['Date']>=start_day]
    train_data=data['Date']
    #data['Date']=data['Date'].apply(lambda x:datetime.strptime(x,'%d/%m/%Y %H:%M:%S'))
    train_data=data[data['Date'] >= start_day]# and data['Date'] <= end_train]
    train_data=train_data[data['Date'] < end_train]
    val_data=data[data['Date'] >= start_val]# and data['Date'] <= end_train]
    val_data=val_data[data['Date'] < end_val]
    rest_data=data[data['Date'] >= end_val]
    rest_data=rest_data[data['Date'] < (forecast_day)]
   
    #val_data=data[data['Date'] >= start_val and data['Date'] <= end_val]

    return train_data,val_data,rest_data