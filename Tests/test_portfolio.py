#!/usr/bin/env python
# coding: utf-8

# In[13]:


import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.append(os.path.abspath(os.path.join('..')))

from portfolio_analysis import load_and_prepare_data, plot_portfolio_distribution

def test_load_and_prepare_data():
    df, portfolio_value, portfolio_returns_clipped = load_and_prepare_data('portfolio_data.db')

    assert not df.empty
    assert not portfolio_value.empty
    assert not portfolio_returns_clipped.empty

def test_plot_portfolio_distribution():
    # Создаем фейковые доходности для теста
    fake_returns = pd.Series(np.random.normal(0, 0.01, 1000)).clip(-1, 3)
    try:
        plot_portfolio_distribution(fake_returns)
    except Exception as e:
        pytest.fail(f"plot_portfolio_distribution вызвала исключение: {e}")


# In[15]:


import sys
import os
sys.path.append('/Users/egorzubkov/Desktop/portfolio-analysis')

from bond_utils import load_bond_data, calc_all_ytm  # импорт твоих функций

def main(args=None):
    parser = argparse.ArgumentParser(description="Portfolio Analysis CLI")
    parser.add_argument(
        "command",
        choices=["analyze-portfolio", "plot-distribution", "analyze-bonds"],  # добавил новую команду
        help="Команда для запуска анализа или построения графика"
    )

    if args is None:
        args = sys.argv[1:]
    args = parser.parse_args(args)

    if args.command == "analyze-portfolio":
        # твой код анализа портфеля
        ...

    elif args.command == "plot-distribution":
        # твой код для графика
        ...

    elif args.command == "analyze-bonds":
        df_securities = load_bond_data()
        calc_date = "2024-07-01"
        bond_df = calc_all_ytm(df_securities, calc_date)
        print(bond_df[['ticker', 'price', 'face_value', 'ytm']])


# In[ ]:




