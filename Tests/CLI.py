#!/usr/bin/env python
# coding: utf-8

import sys
import os
import argparse

# Добавляем в sys.path родительскую папку, чтобы импортировать bond_utils и portfolio_analysis из корня
sys.path.append(os.path.abspath('..'))

from bond_utils import load_bond_data, calc_all_ytm, plot_ytm_sensitivity
from portfolio_analysis import load_and_prepare_data, plot_portfolio_distribution, load_ticker_to_security_id_map
from hypothesis_test import test_hypotheses_for_stocks

ticker_map = load_ticker_to_security_id_map()

def main(args=None):
    parser = argparse.ArgumentParser(description="Portfolio Analysis CLI")
    parser.add_argument(
        "command",
        choices=["analyze-portfolio", "plot-distribution", "analyze-bonds", "test-hypothesis"],
        help="Команда для запуска анализа или построения графика"
    )

    if args is None:
        args = sys.argv[1:]
    args = parser.parse_args(args)

    if args.command == "analyze-portfolio":
        # Код анализа портфеля
        df, portfolio_value, portfolio_returns_clipped = load_and_prepare_data()
        print("Portfolio loaded and processed.")
        print(df.head())
        # Здесь можно добавить дополнительный вывод или действия

    elif args.command == "plot-distribution":
        # Код для построения графика распределения доходности портфеля
        _, _, portfolio_returns_clipped = load_and_prepare_data()
        plot_portfolio_distribution(portfolio_returns_clipped)

    elif args.command == "analyze-bonds":
        # Запуск анализа облигаций
        df_securities = load_bond_data()
        calc_date = "2024-07-01"
        bond_df = calc_all_ytm(df_securities, calc_date)
        print(bond_df[['ticker', 'price', 'face_value', 'ytm']])

        # Вызов графика для первой облигации из таблицы:
        plot_ytm_sensitivity(bond_df.iloc[0])

    elif args.command == "test-hypothesis":
        df, _, _ = load_and_prepare_data()
        # Пример тикеров security_id из ваших данных:
        security1 = ticker_map.get('USBND786')
        security2 = ticker_map.get('EUBND751')

        if security1 is None or security2 is None:
            print("Не найдены security_id для заданных тикеров")
        else:
            test_hypotheses_for_stocks(df, security1, security2)

if __name__ == "__main__":
    main()