# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 22:54:42 2021

@author: ZhangQi
"""


 
 
import yfinance as yf
import datetime as dt
from datetime import date
import matplotlib.pyplot as plt
import yahoo_fin.stock_info as si
import pandas as pd
import numpy as np
import streamlit as st
from pandas_datareader import data
st.set_page_config(page_title="投资分析-Bband indicator",page_icon="🧊",layout="wide")

df_cc = pd.read_csv("china_concept.csv",encoding="GB2312")
tickers = list(df_cc.Ticker2)
names = list(df_cc.Name)

years = [2021]
months = list(range(1,13))
days = list(range(1,31))
periods = [10,20,30]


ticker = st.sidebar.selectbox(
    '常关注的一些股票代码：',
     tickers)   

year = st.sidebar.selectbox(
    '选择开始的年份：一般选择2021年',
     years)  

month = st.sidebar.selectbox(
    '选择开始的月份',
     months) 

day = st.sidebar.selectbox(
    '选择开始的日期',
     days) 

period = st.sidebar.selectbox(
    '选择多少天作为基准来计算区间--一般选择20天',
     periods) 

start = dt.datetime(year, month, day)
end = date.today()

stock = yf.Ticker(ticker)
info = stock.info

name = names[tickers.index(ticker)]

st.title(name)


st.subheader(info['longName']) 
#st.markdown('** Sector **: ' + info['sector'])
#st.markdown('** Industry **: ' + info['industry'])
#st.markdown('** Phone **: ' + info['phone'])
#st.markdown('** Address **: ' + info['address1'] + ', ' + info['city'] + ', ' + info['zip'] + ', '  +  info['country'])
#st.markdown('** Website **: ' + info['website'])
st.info(info['longBusinessSummary'])


st.markdown('** 当黑色线低于绿色线，代表价格过高，是买点；当黑色线高于蓝色线，代表价格过高，是卖点 ** ')

df= stock.history(ticker, start=start, end=end)

multiplier = 2
df['up_band'] = df['Close'].rolling(period).mean() + df['Close'].rolling(period).std() * multiplier
df['mid_band'] = df['Close'].rolling(period).mean()
df['low_band'] = df['Close'].rolling(period).mean() - df['Close'].rolling(period).std() * multiplier


df[['Close','up_band','mid_band','low_band']].plot(figsize= (12,10))
fig, ax = plt.subplots()
#fig = plt.figure(figsize=(12,4)) 
ax.plot(df.index, df['up_band'], linewidth=1.0, linestyle="-",label="上界线")
ax.plot(df.index, df['Close'], linewidth=1.2,color='black',label="收盘价")
ax.plot(df.index, df['mid_band'], linewidth=1.0, linestyle="-",label="中界线")
ax.plot(df.index, df['low_band'], linewidth=1.0, linestyle="-",label="下界线")
ax.fill_between(df.index, df['up_band'],df['low_band'],alpha=.2, linewidth=0)
#plt.axis('tight')
plt.tick_params(axis='x', labelsize=8,rotation=15) 

try:
  indicators = ['marketCap','trailingPE','priceToSalesTrailing12Months','totalRevenue','revenuePerShare','revenueGrowth','returnOnEquity',"grossMargins","profitMargins"]

  col1, col2, col3 = st.columns(3)
  col1.metric(indicators[0], "{:,.2f}".format(info[indicators[0]]/100000000))
  col2.metric(indicators[1], "{:,.2f}".format(info[indicators[1]]))
  col3.metric(indicators[2], "{:,.2f}".format(info[indicators[2]]))

  col4, col5, col6 = st.columns(3)
  col4.metric(indicators[3], "{:,.2f}".format(info[indicators[3]]/100000000))
  col5.metric(indicators[4], "{:,.2f}".format(info[indicators[4]]))
  col6.metric(indicators[5], "{:,.2f}".format(info[indicators[5]]))

  col7, col8, col9 = st.columns(3)
  col7.metric(indicators[6], "{:,.2f}".format(info[indicators[6]]))
  col8.metric(indicators[7], "{:,.2f}".format(info[indicators[7]]))
  col9.metric(indicators[8], "{:,.2f}".format(info[indicators[8]]))
except:
  continue
st.pyplot(fig)




