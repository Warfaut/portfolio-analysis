#!/usr/bin/env python
# coding: utf-8

# In[16]:


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


# In[ ]:




