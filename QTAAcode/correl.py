from pandas import Series, DataFrame
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# This module computes and plots VRP and price correlation on different lags

# Define asset classes and folder name
assetClass = {'China':'China', 'Emg':'Emerging Market', 'FI10':'FI 10yr', 'Gold':'Gold', 'Oil':'Oil','Russel':'Russel 2000', 'SP':'S&P',}

China = pd.read_csv('VRPs/China.csv', index_col='Date')
Emg = pd.read_csv('VRPs/Emg.csv', index_col='Date')
FI10 = pd.read_csv('VRPs/FI10.csv', index_col='Date')
Gold = pd.read_csv('VRPs/Gold.csv', index_col='Date')
Oil = pd.read_csv('VRPs/Oil.csv', index_col='Date')
Russel = pd.read_csv('VRPs/Russel.csv', index_col='Date')
SP = pd.read_csv('VRPs/SP.csv', index_col='Date')

China.index = pd.to_datetime(China.index)
Emg.index = pd.to_datetime(Emg.index)
FI10.index = pd.to_datetime(FI10.index)
Gold.index = pd.to_datetime(Gold.index)
Oil.index = pd.to_datetime(Oil.index)
Russel.index = pd.to_datetime(Russel.index)
SP.index = pd.to_datetime(SP.index)

China['Return'] = (China.Price / China.Price.shift(1) - 1)
Emg['Return'] = (Emg.Price / Emg.Price.shift(1) - 1)
FI10['Return'] = (FI10.Price / FI10.Price.shift(1) - 1)
Gold['Return'] = (Gold.Price / Gold.Price.shift(1) - 1)
Oil['Return'] = (Oil.Price / Oil.Price.shift(1) - 1)
Russel['Return'] = (Russel.Price / Russel.Price.shift(1) - 1)
SP['Return'] = (SP.Price / SP.Price.shift(1) - 1)


# China corre
Correl = dict()
for i in range(1,13):
    Correl[i] = China.VRP.shift(i).corr(China.Return)

ChinaCorrel = Series(Correl)
ChinaCorrel.name = 'China'
#ChinaCorrel.plot()

# Emg corre
Correl = dict()
for i in range(1,13):
    Correl[i] = Emg.VRP.shift(i).corr(Emg.Return)

EmgCorrel = Series(Correl)
EmgCorrel.name = 'Emg'
#EmgCorrel.plot()

# FI10 corre
Correl = dict()
for i in range(1,13):
    Correl[i] = FI10.VRP.shift(i).corr(FI10.Return)

FI10Correl = Series(Correl)
FI10Correl.name = 'FI10'
#FI10Correl.plot()

# Gold corre
Correl = dict()
for i in range(1,13):
    Correl[i] = Gold.VRP.shift(i).corr(Gold.Return)

GoldCorrel = Series(Correl)
GoldCorrel.name = 'Gold'
#GoldCorrel.plot()

# SP corre
Correl = dict()
for i in range(1,13):
    Correl[i] = SP.VRP.shift(i).corr(SP.Return)

SPCorrel = Series(Correl)
SPCorrel.name = 'SP'
#SPCorrel.plot()

# Russel corre
Correl = dict()
for i in range(1,13):
    Correl[i] = Russel.VRP.shift(i).corr(Russel.Return)

RusselCorrel = Series(Correl)
RusselCorrel.name = 'Russel'
#RusselCorrel.plot()

# Oil corre
Correl = dict()
for i in range(1,13):
    Correl[i] = Oil.VRP.shift(i).corr(Oil.Return)

OilCorrel = Series(Correl)
OilCorrel.name = 'Oil'
#OilCorrel.plot()

CORRELATION = pd.concat([ChinaCorrel, EmgCorrel, FI10Correl, GoldCorrel, OilCorrel, RusselCorrel, SPCorrel],axis = 1)



CORRELATION.plot()
plt.title('VRP Return Correlation', color='black')
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.savefig('correlation.pdf')
plt.show()
