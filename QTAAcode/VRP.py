from pandas import Series, DataFrame
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def getDatetime(date):
    return datetime(int(date.split('/')[2]),int(date.split('/')[0]),int(date.split('/')[1]))


def closestDay(date):
    pass
       

VIX = pd.read_csv('vixcurrent.csv', index_col='Date')
SP500 = pd.read_csv('SP500.csv', index_col='Date')
Date = VIX.index
# Compute SP500 daily log return
SPLogReturn = Series((np.log(SP500 / SP500.shift(1)))['Adj Close'])
SPLogReturn.name = 'LogRET'

# Define realized variance series
realizedVar = DataFrame(columns = ['RV'], index = VIX.index)
RV = realizedVar.RV

# Compute the one-month realized variance for each day
# Calculating method is to sum all daily return squares in last 30 days
for date in RV.index:
    sum = 0
    # First we need to insure that all variances shoule be calculated more than  
    # 30 days from beginning, otherwise data will not be precise
    interval = getDatetime(date) - getDatetime(Date[0])
    if  interval.days > 31:
        # summing last 30 day variance
        for day in RV.index:
            interval = getDatetime(date) - getDatetime(day)
            if interval.days <= 30 and interval.days >=0 :
                sum = sum + SPLogReturn[day] ** 2
        RV.set_value(date, sum)
        
# Compute implied variance by VIX. VIX index is presented in percentage,
# so we first need to divide 100 to derive volatility, then get monthly variance
IV = (VIX['VIX Close'].values / 100) ** 2 / 12 

# Here 1 means one DAY lag (first issue: should we build the model in daily basis or monthly?)
VRP = IV - RV.shift(1)

# Here 82 is the lag that I have tested to be highest correlation coefficient
result = pd.concat([VRP.shift(82), SP500['Adj Close']], axis = 1)
result = result.dropna()
result.columns = ['VRP', 'SP500']
result = pd.concat([pd.to_numeric(result.VRP), result.SP500], axis = 1)
print('Correlation coefficient is : ' + str(result.VRP.corr(result.SP500)))

# Plot VRP and SP500 figure
plt.figure()
result.VRP.plot()
result.SP500.plot(secondary_y=True)

# Test correlation in different prediction lag, then plot figure
dayCor = dict()
for i in range(360):
    result = pd.concat([VRP.shift(i), SP500['Adj Close']], axis = 1)
    result = result.dropna()
    result.columns = ['VRP', 'SP500']
    result = pd.concat([pd.to_numeric(result.VRP), result.SP500], axis = 1)
#    print('Correlation coefficient is : ' + str(result.VRP.corr(result.SP500)))
    dayCor[i] = result.VRP.corr(result.SP500)
test = Series(dayCor)
plt.figure()
test.plot()