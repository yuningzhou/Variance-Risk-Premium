from pandas import Series, DataFrame
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define asset classes and folder name
assetClass = {'China':'China', 'Emg':'Emerging Market', 'FI10':'FI 10yr', 'Gold':'Gold', 'Oil':'Oil','Russel':'Russel 2000', 'SP':'S&P',}

test = 'China'

# Compute VRP for each asset classes

# China market
assetName = 'China'
VOL = pd.read_csv('Data/'+assetClass[assetName]+'/vol.csv', index_col='Date')
VOL.index = pd.to_datetime(VOL.index)
Price = pd.read_csv('Data/'+assetClass[assetName]+'/price.csv', index_col='Date')
Price.index = pd.to_datetime(Price.index)

# Get price months
PMonth = []
for i in Price.index:
    if datetime(i.year,i.month,1) not in PMonth:
        PMonth.append(datetime(i.year,i.month,1))

# Get vol months
VMonth = []
for i in VOL.index:
    if datetime(i.year,i.month,1) not in VMonth:
        VMonth.append(datetime(i.year,i.month,1))
        
# Log return
LogReturn = np.log(Price / Price.shift(1))
LogReturn = LogReturn.rename(columns = {'Price':'LogRET'})
# Realized variance
realizedVar = DataFrame(columns = ['RV'], index = PMonth)

for date in realizedVar.index:
    sum = 0
    for i in LogReturn.index:
        if i.year == date.year and i.month == date.month:
                sum = sum + LogReturn.LogRET[i] ** 2
    realizedVar.RV.set_value(date, sum)
# Implied variance
impliedVar = DataFrame(columns = ['IV'], index = VMonth)
for date in impliedVar.index:
    temp = 0
    for i in VOL.index:
        if i.year == date.year and i.month == date.month:
            temp = VOL.Vol[i]
    impliedVar.IV.set_value(date, temp)
    
impliedVar = (impliedVar / 100) ** 2 / 12

# VRP
VRP = impliedVar.IV - realizedVar.RV.shift(1)
VRP.name = 'VRP'
# Final result, price and VRP
China = pd.concat([Price,VRP],axis=1)
China = China.dropna()