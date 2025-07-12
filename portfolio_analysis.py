#!/usr/bin/env python
# coding: utf-8

# In[1]:


# portfolio_analysis.py

import sqlite3
import pandas as pd
import yfinance as yf
from datetime import datetime
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt


def load_ticker_to_security_id_map(db_path='portfolio_data.db'):
    conn = sqlite3.connect(db_path)
    df_securities = pd.read_sql("SELECT id as security_id, ticker FROM securities", conn)
    conn.close()
    return dict(zip(df_securities['ticker'], df_securities['security_id']))

def load_and_prepare_data(db_path='portfolio_data.db'):
    """
    Загружает и подготавливает данные из базы.
    Возвращает DataFrame, стоимость портфеля и очищенные доходности.
    """
    conn = sqlite3.connect(db_path)
    df_portfolio = pd.read_sql("SELECT * FROM portfolio;", conn)
    df_prices = pd.read_sql("SELECT * FROM prices;", conn)
    df_securities = pd.read_sql("SELECT * FROM securities;", conn)

    df = df_portfolio.merge(df_prices, on=['date', 'security_id'], how='left')
    df = df.merge(df_securities[['id', 'currency']], left_on='security_id', right_on='id', how='left')
    df.drop(columns=['id'], inplace=True)

    currencies = df['currency'].dropna().unique()
    currencies = [c for c in currencies if c != 'USD']

    df['date'] = pd.to_datetime(df['date'])
    date_min = df['date'].min().strftime('%Y-%m-%d')
    date_max = df['date'].max().strftime('%Y-%m-%d')

    fx_dfs = []
    for curr in currencies:
        ticker = f"{curr}USD=X"
        pair = yf.Ticker(ticker)
        hist = pair.history(start=date_min, end=date_max)
        df_curr = hist[['Close']].reset_index()
        df_curr.rename(columns={'Date':'date', 'Close':'fx_to_usd'}, inplace=True)
        df_curr['currency'] = curr
        df_curr['date'] = df_curr['date'].dt.date
        fx_dfs.append(df_curr)

    fx_df = pd.concat(fx_dfs, ignore_index=True)

    df['date'] = df['date'].dt.date
    df = df.merge(fx_df, on=['date', 'currency'], how='left')
    df['fx_to_usd'] = df['fx_to_usd'].fillna(1.0)

    df['price_usd'] = df['price'] * df['fx_to_usd']
    df['position_value'] = df['quantity'] * df['price_usd']
    portfolio_value = df.groupby('date')['position_value'].sum().sort_index()

    filtered_value = portfolio_value[portfolio_value > 1000]
    portfolio_returns = filtered_value.pct_change().dropna()
    portfolio_returns_clipped = portfolio_returns.clip(lower=-1, upper=3)

    return df, portfolio_value, portfolio_returns_clipped


def plot_portfolio_distribution(portfolio_returns_clipped):
    """
    Строит графики распределения доходности портфеля с VaR и CVaR.
    """
    alpha = 0.05
    mu = portfolio_returns_clipped.mean()
    sigma = portfolio_returns_clipped.std()
    z = norm.ppf(alpha)

    var_hist = portfolio_returns_clipped.quantile(alpha)
    cvar_hist = portfolio_returns_clipped[portfolio_returns_clipped <= var_hist].mean()
    var_param = mu + z * sigma
    cvar_param = mu - sigma * norm.pdf(z) / alpha

    plt.figure(figsize=(8, 4))
    portfolio_returns_clipped.hist(bins=40, alpha=0.7)
    plt.axvline(var_hist, color='red', linestyle='--', label='VaR 95% (hist)')
    plt.axvline(cvar_hist, color='purple', linestyle=':', label='CVaR 95% (hist)')
    plt.axvline(var_param, color='blue', linestyle='--', label='VaR 95% (param)')
    plt.axvline(cvar_param, color='green', linestyle=':', label='CVaR 95% (param)')
    plt.title("Распределение доходности портфеля (очищенное)")
    plt.xlabel("Доходность")
    plt.ylabel("Частота")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("var_cvar_hist_param_cleaned.png", dpi=300)
    plt.show()


# In[ ]:




