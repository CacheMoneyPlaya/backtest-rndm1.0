from __future__ import (absolute_import, division, print_function, unicode_literals)
import datetime
import os.path
import sys
import pandas as pd
from Strategies.FVG.FvgHost import FvgHost
import backtrader as bt
import Datasets.CSVExecutables.scrape_ohlc_data as data_scraper
import Datasets.CSVExecutables.unix_to_datetime as unix_converter
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-a", "--asset", help="Asset to backtest", required=True)
    parser.add_argument("-t", "--timeframe", help="OHLC Timeframe i.e. 1m,5m,15m..", required=True)
    parser.add_argument("-d", "--starting_date", help="Datascrape start date i.e. '2020-05-20'", required=True)
    parser.add_argument("-e", "--exchange", help="Exchange i.e. binance, ftx, bitmex", required=True)
    parser.add_argument("-r", "--reuse_data", help="Reuse saved data for asset", required=False, action="store_true")

    args, unknown = parser.parse_known_args()
    config = vars(args)

    data_scraper.data_setup(config)

    cerebro = bt.Cerebro()
    cerebro.addstrategy(FvgHost)

    modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    datapath = os.path.join(modpath, 'Datasets/Data/' + config['asset'] + '_' + config['exchange'] + '_datetime.csv')

    start_date = config['starting_date'].split('-')
    end_date = datetime.datetime.today().strftime('%Y-%m-%d').split('-')

    data = bt.feeds.GenericCSVData(
            dataname=datapath,
            fromdate=datetime.datetime(int(start_date[0]), int(start_date[1]), int(start_date[2])),
            todate=datetime.datetime(int(end_date[0]), int(end_date[1]), int(end_date[2])),
            nullvalue=0.0,
            dtformat='%Y-%m-%d %H:%M:%S',
            timeframe=bt.TimeFrame.Minutes,
            datetime=0,
            open=1,
            high=2,
            low=3,
            close=4,
            volume=5,
            openinterest=-1
        )

    cerebro.adddata(data)
    cerebro.broker.setcash(1000.0)
    cerebro.broker.set_shortcash(False)
    cerebro.broker.setcommission(commission=0.0015, margin = None, mult = 10)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
