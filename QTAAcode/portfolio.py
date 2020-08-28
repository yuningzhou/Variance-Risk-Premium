from pandas import Series, DataFrame
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def rank_to_weight(rank):
    for i in rank:
        if i <= 2:
            i = -0.5
        else:
            i = 0.5
    return rank

            
equity = pd.read_csv('data/equity_VRP.csv', index_col='Date')
equity.index = pd.to_datetime(equity.index)

fixincome = pd.read_csv('data/fixincome_VRP.csv', index_col='Date')
fixincome.index = pd.to_datetime(fixincome.index)

gold = pd.read_csv('data/gold_VRP.csv', index_col='Date')
gold.index = pd.to_datetime(gold.index)

oil = pd.read_csv('data/oil_VRP.csv', index_col='Date')
oil.index = pd.to_datetime(oil.index)


VRP = pd.concat([equity.VRP, fixincome.VRP, gold.VRP, oil.VRP],axis = 1)
VRP.columns = ['equity', 'fixincome', 'gold', 'oil']

price = pd.concat([equity.SP500, fixincome.SP500, gold.SP500, oil.SP500],axis = 1)
price.columns = ['equity', 'fixincome', 'gold', 'oil']

VRP = VRP.dropna()
price = price.dropna()

position = VRP.rank(axis = 1)
position = DataFrame(columns = ['equity', 'fixincome', 'gold', 'oil'] , index = price.index)

position = VRP.rank(axis = 1)

for asset in position:
    position[asset] = np.where(position[asset] <=2, -0.5, 0.5)

position1 = position.shift(1)
position1 = position1.fillna(0)
trade = position - position1

# initial investment
iniInv = 100
value = Series(index = trade.index)
value.ix[0] = iniInv

price1 = price.shift(1)
priceChange = (price - price1) / price
position = position.shift(3)
for i in trade.index:
    if i != trade.index[0]:
        temp = priceChange[priceChange.index==i]*position[position.index==i]
        value[value.index == i] =  value.ix[(trade.index.get_loc(i)-1)]*(1+temp.sum().sum())

value.plot()
