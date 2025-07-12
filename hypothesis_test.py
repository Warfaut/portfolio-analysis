#!/usr/bin/env python
# coding: utf-8

# In[15]:


from scipy.stats import ttest_ind, levene
import pandas as pd

def prepare_returns(df):
    # Считаем доходности (pct_change) для каждой акции (security_id)
    df = df.sort_values(['security_id', 'date'])
    df['returns'] = df.groupby('security_id')['price_usd'].pct_change()
    return df

def test_hypotheses_for_stocks(df, security1, security2):
    df = prepare_returns(df)

    returns_1 = df[df['security_id'] == security1]['returns'].dropna()
    returns_2 = df[df['security_id'] == security2]['returns'].dropna()

    print(f"Returns 1 ({security1}):", returns_1.head())
    print(f"Returns 2 ({security2}):", returns_2.head())
    print(f"Размер выборки 1: {len(returns_1)}, Размер выборки 2: {len(returns_2)}")

    if len(returns_1) == 0 or len(returns_2) == 0:
        print("Одна из выборок пустая, тест провести нельзя.")
        return

    stat_levene, p_levene = levene(returns_1, returns_2)
    stat_ttest, p_ttest = ttest_ind(returns_1, returns_2, equal_var=(p_levene > 0.05))

    print(f"Levene test: stat={stat_levene:.4f}, p={p_levene:.4f}")
    print(f"T-test: stat={stat_ttest:.4f}, p={p_ttest:.4f}")

    if p_levene < 0.05:
        print("Дисперсии статистически различаются.")
    else:
        print("Дисперсии не различаются.")

    if p_ttest < 0.05:
        print("Средние статистически различаются.")
    else:
        print("Средние не различаются.")


# In[ ]:




