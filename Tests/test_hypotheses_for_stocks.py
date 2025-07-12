#!/usr/bin/env python
# coding: utf-8

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pandas as pd
from hypothesis_test import test_hypotheses_for_stocks

class TestHypothesis(unittest.TestCase):

    def setUp(self):
        # Создаем искусственный DataFrame с доходностями для двух security_id
        data = {
            'security_id': [1]*10 + [2]*10,
            'date': pd.date_range('2024-01-01', periods=10).tolist()*2,
            'price_usd': list(range(10, 20)) + list(range(20, 30))
        }
        self.df = pd.DataFrame(data)

    def test_equal_means_variances(self):
        # Тест для выборок с одинаковыми средними и дисперсиями
        self.df.loc[self.df['security_id'] == 2, 'price_usd'] = range(10, 20)
        test_hypotheses_for_stocks(self.df, 1, 2)  # Просто вызов — вывод в консоль

    def test_different_means(self):
        # Смещаем вторую выборку, чтобы средние были разными
        self.df.loc[self.df['security_id'] == 2, 'price_usd'] = range(20, 30)
        test_hypotheses_for_stocks(self.df, 1, 2)  # Вывод в консоль с различиями

    def test_empty_sample(self):
        # Проверяем обработку пустой выборки
        empty_df = self.df[self.df['security_id'] == 1].copy()
        test_hypotheses_for_stocks(empty_df, 1, 99)  # 99 — несуществующий id

if __name__ == "__main__":
    unittest.main()