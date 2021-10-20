# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 06:03:32 2021

@author: Hamzah
"""


import pandas as pd
raw_data=pd.read_excel('features.xlsx')

from datetime import datetime
import numpy as np
from data_rf_ext import data_ext
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib 
import os
#raw_data=pd.read_csv("data.csv")
forecast_day='15-04-2020 00:00:00'



train_data=pd.read_excel('data.xlsx')


from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
X = train_data.iloc[:,1:10]
Y= train_data.iloc[:,-1] 
X_t=X.copy()
col=X_t.columns.tolist()
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))

for i in col:
    X_t[i]=sc.fit_transform(np.asarray(X_t[i]).reshape(-1,1))
    
    


from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt
model = ExtraTreesClassifier()
model.fit(X_t.iloc[1:300],Y.iloc[1:300])
#print(model.feature_importances_)
feat_importances = pd.Series(model.feature_importances_, index=X_t.columns)
feat_importances=feat_importances*100
#feat_importances.nlargest(10).plot(kind='barh',color='maroon')
#ax = feat_importances.plot(figsize=(12,10))#,marker='.',markersize=15)
ax=feat_importances.nlargest(10).plot(kind='barh',color='thistle',figsize=(19,10))

ax.set_xlabel("Impact on model (%)",fontsize=18)
#ax.set_ylabel("Irradiance (W⋅m−2)",fontsize=12)
#ax.set_title('Feature importance',fontsize=15);
plt.xticks(fontsize=15) 
plt.yticks(fontsize=15) 
#plt.legend(loc=2, prop={'size':16})
#plt.grid()
plt.savefig('best features.svg', dpi=600, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0,
        frameon=None, metadata=None)
