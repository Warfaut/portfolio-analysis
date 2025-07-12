#!/usr/bin/env python
# coding: utf-8

# In[20]:


# cli.py

import argparse
import sys
from portfolio_analysis import load_and_prepare_data, plot_portfolio_distribution

def main(args=None):
    parser = argparse.ArgumentParser(description="Portfolio Analysis CLI")
    parser.add_argument(
        "command",
        choices=["analyze-portfolio", "plot-distribution"],
        help="Команда для запуска анализа или построения графика"
    )

    if args is None:
        args = sys.argv[1:]  # аргументы из командной строки
    args = parser.parse_args(args)

    if args.command == "analyze-portfolio":
        df, portfolio_value, portfolio_returns_clipped = load_and_prepare_data()
        print("Portfolio loaded and processed.")
    elif args.command == "plot-distribution":
        _, _, portfolio_returns_clipped = load_and_prepare_data()
        plot_portfolio_distribution(portfolio_returns_clipped)

if __name__ == "__main__":
    main()


# In[ ]:




