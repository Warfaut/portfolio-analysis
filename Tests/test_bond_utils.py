#!/usr/bin/env python
# coding: utf-8

# In[5]:


import sys
import os
import pytest

# Добавляем родительскую папку (portfolio-analysis) в sys.path
sys.path.append(os.path.abspath('..'))

from bond_utils import load_bond_data, compute_ytm, calc_all_ytm

def test_load_bond_data():
    df = load_bond_data()
    assert not df.empty, "Данные облигаций не должны быть пустыми"
    assert 'payment_schedule' in df.columns, "В данных должна быть колонка payment_schedule"

def test_compute_ytm():
    # Тестовые данные для расчёта YTM
    payment_schedule_json = '{"schedule":[{"date":"2025-07-01","amount":5},{"date":"2026-07-01","amount":105}]}'
    ytm = compute_ytm(
        calc_date="2024-07-01",
        price=100,
        face_value=100,
        payment_schedule_json=payment_schedule_json
    )
    assert ytm is not None, "YTM должен быть рассчитан"
    assert 0 < ytm < 1, "YTM должен быть в разумных пределах (0 < ytm < 1)"

def test_calc_all_ytm():
    df = load_bond_data()
    calc_date = "2024-07-01"
    bond_df = calc_all_ytm(df, calc_date)
    assert 'ytm' in bond_df.columns, "В результате должен быть столбец ytm"
    assert not bond_df['ytm'].isnull().all(), "YTM должен быть рассчитан хотя бы для одной облигации"


# In[ ]:




