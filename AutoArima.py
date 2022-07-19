import pmdarima as pm
import pandas as pd
import numpy as np

class auto_arima:
    
    def __init__(self,train,test,timesteps,H,alpha):
        self.train=train
        self.test=test
        self.timesteps=timesteps
        self.H=H
        self.alpha=alpha
    
    def fit(self):

        model = pm.auto_arima(self.train,
                      m=1,             
                      d=None,           
                      seasonal=False,   
                      start_P=0, 
                      D=None,
                      max_order =None, 
                      trace=True,
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=True)
        return model
    def summary_statistics(self,arr):
    # calculates summary statistics from array
    
        return [np.quantile(arr,0.5),np.quantile(arr,0.75)-np.quantile(arr,0.25)]

    def calculate_metrics(self):
        model=self.fit()
        fc, confint = model.predict(n_periods=self.H, return_conf_int=True,alpha=self.alpha)

        lower_bound = confint[:, 0].flatten()
        upper_bound = confint[:, 1].flatten()

        interval_width=np.abs(upper_bound-lower_bound)
        counter=0

        for i in range(self.H):
            if self.test[i] >= lower_bound[i] and self.test[i] <= upper_bound[i]:
                counter+=1
        
        return counter/self.H,self.summary_statistics(interval_width)