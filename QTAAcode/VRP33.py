from pandas import Series, DataFrame
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Portfolio without FI10

China = pd.read_csv('VRPs/China.csv', index_col='Date')
Emg = pd.read_csv('VRPs/Emg.csv', index_col='Date')
#FI10 = pd.read_csv('VRPs/FI10.csv', index_col='Date')
Gold = pd.read_csv('VRPs/Gold.csv', index_col='Date')
Oil = pd.read_csv('VRPs/Oil.csv', index_col='Date')
Russel = pd.read_csv('VRPs/Russel.csv', index_col='Date')
SP = pd.read_csv('VRPs/SP.csv', index_col='Date')

China.index = pd.to_datetime(China.index)
Emg.index = pd.to_datetime(Emg.index)
#FI10.index = pd.to_datetime(FI10.index)
Gold.index = pd.to_datetime(Gold.index)
Oil.index = pd.to_datetime(Oil.index)
Russel.index = pd.to_datetime(Russel.index)
SP.index = pd.to_datetime(SP.index)

# Concat all vrps and prices together
VRP = pd.concat([China.VRP, Emg.VRP, Gold.VRP, Oil.VRP, Russel.VRP, SP.VRP], axis = 1)
VRP.columns = ['China','Emg','Gold','Oil','Russel','SP']
VRP = VRP.dropna()
Price = pd.concat([China.Price, Emg.Price, Gold.Price, Oil.Price, Russel.Price, SP.Price], axis = 1)
Price.columns = ['China','Emg','Gold','Oil','Russel','SP']
Price = Price.dropna()

position = VRP.rank(axis = 1)

for i in position:
    for j in range(len(position)):
        if position[i].ix[j] == 1 or position[i].ix[j] == 2 or position[i].ix[j] == 3 :
            position[i].ix[j] = -1/3
        elif position[i].ix[j] == 5 or position[i].ix[j] == 6 or position[i].ix[j] == 4:
            position[i].ix[j] = 1/3

# position at next time point, used to calculate position changes
# in the correlation charts, correlation are highest on 4month lag.
position1 = position.shift(4) 

# return 
priceChange = (Price - Price.shift(1)) / Price

# initial investment
iniInv = 100
value = Series(index = position.index)
value.ix[0] = iniInv


# idea for calculating portfolio:
# at each time point, for each asset class, multiply its return and position weight. summing all win and losses we get
# update on total portfolio
for i in position.index:
    if i != position.index[0]:
        temp = priceChange[priceChange.index==i]*position1[position1.index==i]
        value[value.index == i] =  value.ix[(position.index.get_loc(i)-1)]*(1+temp.sum().sum())

value.plot()

# set up portfolio benchmark (6 asset equal weight)
bmPosition = position.copy()
for i in bmPosition:
    for j in range(len(bmPosition)):
        bmPosition[i].ix[j] = 1 / 6

# benchmark value
bmValue = Series(index = position.index)
bmValue.ix[0] = iniInv

# Calculate benchmark 
for i in bmPosition.index:
    if i != bmPosition.index[0]:
        temp = priceChange[priceChange.index==i]*bmPosition[bmPosition.index==i]
        bmValue[bmValue.index == i] =  bmValue.ix[(bmPosition.index.get_loc(i)-1)]*(1+temp.sum().sum())

value.plot()

compare = pd.concat([value, bmValue], axis = 1)
compare.columns=['VRP', 'Benchmark']
compare.plot()