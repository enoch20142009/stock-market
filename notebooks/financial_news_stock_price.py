#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/enoch20142009/stock-market/blob/main/notebooks/financial_news_stock_price.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Import Packages

# In[ ]:


# IMPORTS
import numpy as np
import pandas as pd
import requests
from io import StringIO
import json

#Fin Data Sources
import yfinance as yf
import time
from datetime import date


# # Ingest Datasets

# In[ ]:


# Extract AAPL, MSFT, TSLA price information from yfinance
tickers = ['AAPL', 'MSFT', 'TSLA']
stock_df = yf.download(tickers, start="2023-01-01", end="2023-12-31")
stock_df = stock_df.stack(level=1).reset_index().rename(columns={"level_1": "ticker"})

# Log the stock DataFrame
log_audit('stock_df', 'Read in stock_df from yfinance package', stock_df)

#Save the DataFrame to a CSV file for reproducibility
stock_df.to_csv("stock_df.csv", index=False)


# In[ ]:


# Read in financial news dataset
from pandas import json_normalize

with open("polygon_news_sample.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Convert nested JSON news dataset into structured tabular format
exploded_df = df.explode('insights').reset_index(drop=True)
exploded_df = json_normalize(exploded_df['insights'])
news_df = pd.concat([df.drop(columns=['insights']), exploded_df], axis=1)

# Only keep useful columns
news_df = news_df[['published_utc', 'description', 'title', 'ticker', 'sentiment', 'sentiment_reasoning']]
news_df.isnull().any()

# Filter to only 'AAPL', 'MSFT', 'TSLA'
tickers = ['AAPL', 'MSFT', 'TSLA']
filter = news_df['ticker'].isin(tickers)
news_df = news_df[filter]

# Log the stock DataFrame
log_audit('news_df', 'Read in news_df from raw JSON file', news_df)


# # Data Hygiene work

# In[ ]:


# Ensure no missing values/invalid values and set up audit trail to track for deleted rows, remove neutral sentiment
news_df = news_df.dropna()
log_audit('news_df', 'Remove all NaN value and invalid values (if any)', news_df)

# Ensure no invalid values (Validation check)
stock_df = stock_df.dropna()
filter = (stock_df['Close'] > 0) & (stock_df['High'] > 0) & (stock_df['Low'] > 0) & (stock_df['Open'] > 0)& (stock_df['Volume'] > 0)
stock_df = stock_df[filter]
log_audit('stock_df', 'Remove all NaN value and invalid values (if any)', stock_df)


# In[ ]:


# Ensure the consistency of date format in stock_df
stock_df['Date'] = pd.to_datetime(stock_df['Date'])

# Convert date format on news_df_final
news_df['published_utc'] = pd.to_datetime(news_df['published_utc'])
news_df['Date'] = news_df['published_utc'].dt.date
news_df.drop('published_utc', axis=1, inplace=True)
news_df['Date'] = pd.to_datetime(news_df['Date'])
log_audit('news_df', 'Add Date column from published_utc to match the date format of stock_df', news_df)


# In[ ]:


# Drop duplicate just in case of multiple entries and only keep the first news for the day for simplicity
stock_df = stock_df.drop_duplicates(subset=['Date', 'Ticker'])
log_audit('stock_df', 'Remove duplicate rows (if any)', stock_df)

news_df = news_df.drop_duplicates(subset=['Date', 'ticker'])
log_audit('news_df', 'Remove duplicate rows (if any) to just keep one news for each day for simplicity', news_df)


# # Dataset Integration

# In[ ]:


# Merge the two dataset
merged_df = pd.merge(news_df, stock_df, how='inner', left_on=['ticker', 'Date'], right_on=['Ticker', 'Date'])

# Add daily difference column
merged_df['daily_diff'] = merged_df['Close'] - merged_df['Open']
merged_df.drop('ticker', axis=1, inplace=True)
log_audit('merged_df', 'Create merged_df by merging stock_df and news_df, also create a column daily_diff to capture daily price movement', merged_df)

# Export the merged dataset into csv
merged_df.to_csv("merged_dataset.csv", index=False)

