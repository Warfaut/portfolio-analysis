#!/usr/bin/env python
# coding: utf-8

# In[65]:


import json
from datetime import datetime
from scipy.optimize import brentq
import pandas as pd
import sqlite3

# --- Функция расчёта YTM ---
def compute_ytm(calc_date, price, face_value, payment_schedule_json):
    schedule = json.loads(payment_schedule_json)["schedule"]
    if isinstance(calc_date, str):
        calc_date = datetime.strptime(calc_date, "%Y-%m-%d")

    coupon_period_days = 180  # Полугодие

    def npv_diff(y):
        total_pv = 0.0
        for payment in schedule:
            pay_date = datetime.strptime(payment["date"], "%Y-%m-%d")
            if pay_date <= calc_date:
                continue
            days_diff = (pay_date - calc_date).days
            t = days_diff / coupon_period_days  # В полугодиях
            amount = float(payment["amount"])
            total_pv += amount / ((1 + y / 2) ** t)
        return total_pv - price

    try:
        ytm = brentq(npv_diff, 1e-6, 1.0)  # Диапазон 0.0001% - 100%
        return ytm
    except ValueError:
        return None

# --- Загрузка данных облигаций ---
def load_bond_data(db_path='portfolio_data.db'):
    conn = sqlite3.connect(db_path)
    df_sec = pd.read_sql("SELECT * FROM securities", conn)
    return df_sec

# --- Расчёт YTM по всем облигациям ---
def calc_all_ytm(df_securities, calc_date):
    bond_df = df_securities[df_securities['security_type_id'] == 2].copy()
    
    bond_prices = pd.read_sql("SELECT * FROM prices", sqlite3.connect('portfolio_data.db'))
    
    bond_df = bond_df.merge(bond_prices[['security_id', 'price']], left_on='id', right_on='security_id', how='left')
    
    bond_df['ytm'] = bond_df.apply(
        lambda row: compute_ytm(
            calc_date,
            row['price'] * row['face_value'] / 100,
            row['face_value'],
            row['payment_schedule']
        ),
        axis=1
    )
    # Можно удалить колонку security_id, если не нужна
    bond_df.drop(columns=['security_id'], inplace=True)
    
    return bond_df
   

# --- Запуск и вывод результата ---
if __name__ == "__main__":
    calc_date = "2024-07-01"
    df_securities = load_bond_data()
    bond_df = calc_all_ytm(df_securities, calc_date)
    print(bond_df[['ticker', 'price', 'face_value', 'ytm']])


# In[67]:


import matplotlib.pyplot as plt
import numpy as np

def plot_ytm_sensitivity(row, price_col='price'):
    base_price = row[price_col]
    prices = np.linspace(base_price * 0.95, base_price * 1.05, 20)
    ytms = [compute_ytm("2024-07-01", price * row['face_value'] / 100, row['face_value'], row['payment_schedule']) for price in prices]

    plt.plot(prices, ytms)
    plt.xlabel("Цена облигации")
    plt.ylabel("Доходность к погашению (YTM)")
    plt.title(f"Чувствительность YTM облигации {row['ticker']}")
    plt.show()



# In[ ]:




