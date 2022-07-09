#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 00:16:25 2022

@author: joshchang0928
"""

import pandas as pd
import yfinance as yf
import numpy as np
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt

def get_stock_price(symbol):
  df = yf.download(symbol, start='2021-02-01', threads= False)
  df['Date'] = pd.to_datetime(df.index)
  df['Date'] = df['Date'].apply(mpl_dates.date2num)
  df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
  return df

def is_support(df, max_list, pivots_s, fig, ax):  
    for i in range(5, len(df)-5):
      # taking a window of 9 candles
      high_range = df['High'][i-5:i+4]
      current_max = high_range.max()
      # if we find a new maximum value, empty the max_list 
      if current_max not in max_list:
          max_list = []
      max_list.append(current_max)
      # if the maximum value remains the same after shifting 5 times
      if len(max_list)==5 and is_far_from_level(current_max,pivots_s,df):
          pivots_s.append((high_range.idxmax(), current_max))
      
def is_resistance(df, min_list, pivots_r, fig, ax):  
    for i in range(5, len(df)-5):
       low_range = df['Low'][i-5:i+4]
       current_min = low_range.min()
       if current_min not in min_list:
           min_list = []
       min_list.append(current_min)
       if len(min_list)==5 and is_far_from_level(current_min,pivots_r,df):
           pivots_r.append((low_range.idxmin(), current_min))

# to make sure the new level area does not exist already
def is_far_from_level(value, levels, df):    
  ave =  np.mean(df['High'] - df['Low'])    
  return np.sum([abs(value-level)<ave for _,level in levels])==0

def plot_all(levels, df, color, fig, ax):    
  candlestick_ohlc(ax,df.values,width=0.6, colorup='green', 
    colordown='red', alpha=0.8)    
  date_format = mpl_dates.DateFormatter('%d %b %Y')
  ax.xaxis.set_major_formatter(date_format)    
  for level in levels:        
    plt.hlines(level[1], xmin = df['Date'][level[0]], xmax = 
      max(df['Date']), colors=color, linestyle='--')    
  fig.show()
  
#method 2: window shifting method
symbol = 'COST'
df = get_stock_price(symbol)
pivots_s = []
pivots_r = []
max_list = []
min_list = []
fig, ax= plt.subplots(figsize=(16, 9))  

is_support(df,max_list,pivots_s, fig, ax)
is_resistance(df,min_list,pivots_r, fig, ax)

plot_all(pivots_s, df, 'blue', fig, ax)
plot_all(pivots_r, df, 'black', fig, ax)



